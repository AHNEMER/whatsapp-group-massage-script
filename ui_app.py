import streamlit as st
import pandas as pd
import os
import json
from pathlib import Path
import time
from send_massage_from_ui import send_messages_from_ui
from phone_extractor import extract_from_uploaded_file, normalize_phone_number

# Language translations
TRANSLATIONS = {
    'ar': {
        'title': '📱 مرسل رسائل واتساب',
        'upload_files': '📤 رفع الملفات',
        'upload_csv_excel': 'رفع ملف CSV/Excel/Numbers يحتوي على أرقام الهواتف',
        'upload_help': 'يجب أن يحتوي الملف على عمود بأرقام الهواتف',
        'or_enter_manually': 'أو أدخل الأرقام يدوياً',
        'enter_numbers': 'أدخل أرقام الهواتف (رقم واحد في كل سطر)',
        'add_numbers': 'إضافة الأرقام',
        'message_content': '📝 محتوى الرسالة',
        'type_message': 'اكتب رسالتك',
        'upload_image': 'رفع صورة (اختياري)',
        'phone_numbers_list': '📋 قائمة أرقام الهواتف',
        'total_numbers': 'إجمالي الأرقام',
        'send_messages': '🚀 إرسال الرسائل',
        'clear_all': '🗑️ مسح الكل',
        'sending_in_progress': '⏳ جاري إرسال الرسائل... يرجى الانتظار',
        'completed_all': '✅ اكتمل! تم إرسال جميع الرسائل بنجاح!',
        'completed_with_errors': '⚠️ اكتمل! نجح: {success}, فشل: {failed}',
        'no_numbers': '❌ يرجى إضافة أرقام الهواتف أولاً!',
        'no_content': '❌ يرجى إدخال رسالة أو رفع صورة!',
        'starting': '🚀 بدء إرسال الرسائل...',
        'tips': '💡 نصائح:',
        'tip1': '- يجب أن تتضمن أرقام الهواتف رمز الدولة (مثل +966 للسعودية)',
        'tip2': '- يمكنك إرسال نص فقط، أو صورة فقط، أو كليهما',
        'tip3': '- تأكد من تسجيل الدخول إلى WhatsApp Web قبل الإرسال',
        'warning_title': '⚠️ تحذير مهم',
        'warning_text': 'يجب إغلاق جميع تبويبات WhatsApp Web قبل البدء!',
        'language': 'اللغة',
        'arabic': 'العربية',
        'english': 'English',
        'pending': '⏸️',
        'sending': '⏳',
        'success': '✅',
        'failed': '❌'
    },
    'en': {
        'title': '📱 WhatsApp Message Sender',
        'upload_files': '📤 Upload Files',
        'upload_csv_excel': 'Upload CSV/Excel/Numbers file with phone numbers',
        'upload_help': 'File should contain phone numbers in a column',
        'or_enter_manually': 'Or Enter Numbers Manually',
        'enter_numbers': 'Enter phone numbers (one per line)',
        'add_numbers': 'Add Manual Numbers',
        'message_content': '📝 Message Content',
        'type_message': 'Type your message',
        'upload_image': 'Upload Image (Optional)',
        'phone_numbers_list': '📋 Phone Numbers List',
        'total_numbers': 'Total numbers',
        'send_messages': '🚀 Send Messages',
        'clear_all': '🗑️ Clear All',
        'sending_in_progress': '⏳ Sending messages in progress... Please wait',
        'completed_all': '✅ Completed! All messages sent successfully!',
        'completed_with_errors': '⚠️ Completed! Success: {success}, Failed: {failed}',
        'no_numbers': '❌ Please add phone numbers first!',
        'no_content': '❌ Please enter a message or upload an image!',
        'starting': '🚀 Starting to send messages...',
        'tips': '💡 Tips:',
        'tip1': '- Phone numbers must include country code (e.g., +966 for Saudi Arabia)',
        'tip2': '- You can send text only, image only, or both',
        'tip3': '- Make sure WhatsApp Web is logged in before sending',
        'warning_title': '⚠️ Important Warning',
        'warning_text': 'All WhatsApp Web tabs must be closed before starting!',
        'language': 'Language',
        'arabic': 'العربية',
        'english': 'English',
        'pending': '⏸️',
        'sending': '⏳',
        'success': '✅',
        'failed': '❌'
    }
}

# Page configuration
st.set_page_config(
    page_title="WhatsApp Message Sender",
    page_icon="📱",
    layout="wide"
)

# Initialize session state
if 'numbers_list' not in st.session_state:
    st.session_state.numbers_list = []
if 'message_text' not in st.session_state:
    st.session_state.message_text = ""
if 'image_file' not in st.session_state:
    st.session_state.image_file = None
if 'sending_status' not in st.session_state:
    st.session_state.sending_status = {}
if 'is_sending' not in st.session_state:
    st.session_state.is_sending = False
if 'language' not in st.session_state:
    st.session_state.language = 'ar'  # Arabic as default

# Get current language translations
lang = st.session_state.language
t = TRANSLATIONS[lang]

# Language switcher in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    language_option = st.radio(
        t['language'],
        options=['ar', 'en'],
        format_func=lambda x: t['arabic'] if x == 'ar' else t['english'],
        index=0 if st.session_state.language == 'ar' else 1
    )
    if language_option != st.session_state.language:
        st.session_state.language = language_option
        st.rerun()

# Warning banner at the top
st.warning(f"⚠️ **{t['warning_title']}**: {t['warning_text']}")

st.title(t['title'])
st.markdown("---")

# Sidebar for file upload and settings
with st.sidebar:
    st.header(t['upload_files'])
    
    # CSV/Excel/Numbers file upload
    uploaded_file = st.file_uploader(
        t['upload_csv_excel'],
        type=['csv', 'xlsx', 'xls', 'numbers'],
        help=t['upload_help'] + (" (CSV, Excel, Apple Numbers)" if lang == 'en' else " (CSV, Excel, Apple Numbers)")
    )
    
    if uploaded_file is not None:
        try:
            # Use phone_extractor module
            numbers = extract_from_uploaded_file(uploaded_file)
            
            if numbers:
                st.session_state.numbers_list = numbers
                st.success(f"✅ {t['success']} تم تحميل {len(numbers)} رقم هاتف" if lang == 'ar' else f"✅ {t['success']} Loaded {len(numbers)} phone numbers")
            else:
                st.error(f"❌ {t['failed']} لم يتم العثور على أرقام هاتف صحيحة" if lang == 'ar' else f"❌ {t['failed']} No valid phone numbers found")
                
        except Exception as e:
            error_msg = str(e)
            # Provide more helpful error messages
            if "No phone number column found" in error_msg:
                st.error(f"❌ {t['failed']} " + ("لم يتم العثور على عمود أرقام الهواتف. " if lang == 'ar' else "No phone number column found. ") + 
                        ("العمود يجب أن يحتوي على: phone, Phone, number, phone number, أو ext" if lang == 'ar' else "Column should contain: phone, Phone, number, phone number, or ext"))
                if "Available columns" in error_msg:
                    st.info("📋 " + ("الأعمدة المتاحة: " if lang == 'ar' else "Available columns: ") + error_msg.split("Available columns: ")[-1] if "Available columns: " in error_msg else "")
            elif "No valid phone numbers found" in error_msg:
                st.error(f"❌ {t['failed']} " + ("لم يتم العثور على أرقام هاتف صحيحة. " if lang == 'ar' else "No valid phone numbers found. "))
                if "Sample values" in error_msg:
                    sample_info = error_msg.split("Sample values: ")[-1] if "Sample values: " in error_msg else ""
                    st.info("💡 " + ("أمثلة على القيم الموجودة: " if lang == 'ar' else "Sample values found: ") + sample_info)
                    st.info("💡 " + ("تأكد من أن الأرقام بصيغة: +966xxxxxxxxx أو 966xxxxxxxxx أو 05xxxxxxxx" if lang == 'ar' else "Ensure numbers are in format: +966xxxxxxxxx, 966xxxxxxxxx, or 05xxxxxxxx"))
            else:
                st.error(f"❌ {t['failed']} " + ("خطأ في قراءة الملف: " if lang == 'ar' else "Error reading file: ") + error_msg)
    
    # Manual number input
    st.markdown("---")
    st.subheader(t['or_enter_manually'])
    manual_numbers = st.text_area(
        t['enter_numbers'],
        height=100,
        help="مثال:\n966505815487\n0551234567\n+966541556250" if lang == 'ar' else "Example:\n966505815487\n0551234567\n+966541556250"
    )
    
    if st.button(t['add_numbers']):
        if manual_numbers:
            # Normalize each number
            numbers = []
            for num in manual_numbers.split('\n'):
                num = num.strip()
                if num:
                    normalized = normalize_phone_number(num)
                    if normalized:
                        numbers.append(normalized)
            
            if numbers:
                st.session_state.numbers_list.extend(numbers)
                st.session_state.numbers_list = list(set(st.session_state.numbers_list))  # Remove duplicates
                st.success(f"✅ {t['success']} تمت إضافة {len(numbers)} رقم" if lang == 'ar' else f"✅ {t['success']} Added {len(numbers)} numbers")
            else:
                st.error(f"❌ {t['failed']} لم يتم العثور على أرقام هاتف صحيحة" if lang == 'ar' else f"❌ {t['failed']} No valid phone numbers found")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header(t['message_content'])
    
    # Message text input
    message_text = st.text_area(
        t['type_message'],
        height=150,
        value=st.session_state.message_text,
        help=t['tip1']
    )
    st.session_state.message_text = message_text
    
    # Image upload
    st.markdown("---")
    uploaded_image = st.file_uploader(
        t['upload_image'],
        type=['jpg', 'jpeg', 'png', 'gif'],
        help=t['tip2']
    )
    
    if uploaded_image is not None:
        st.session_state.image_file = uploaded_image
        # Make image more visible with larger display
        st.markdown("**" + ("معاينة الصورة" if lang == 'ar' else "Image Preview") + ":**")
        # Display image - compatible with all Streamlit versions
        try:
            # Try with use_container_width for newer versions
            st.image(uploaded_image, caption=uploaded_image.name, use_container_width=True)
        except TypeError:
            # Fallback for older Streamlit versions that don't support use_container_width
            st.image(uploaded_image, caption=uploaded_image.name)
    else:
        st.session_state.image_file = None

with col2:
    st.header(t['phone_numbers_list'])
    
    if st.session_state.numbers_list:
        st.info(f"{t['total_numbers']}: {len(st.session_state.numbers_list)}")
        
        # Scrollable list with status
        container = st.container()
        with container:
            for idx, num in enumerate(st.session_state.numbers_list):
                # Get status for this number
                status = st.session_state.sending_status.get(num, "pending")
                
                # Color code based on status
                if status == "success":
                    st.success(f"{t['success']} {num}")
                elif status == "failed":
                    st.error(f"{t['failed']} {num}")
                elif status == "sending":
                    st.warning(f"{t['sending']} {num} ({'جاري الإرسال...' if lang == 'ar' else 'sending...'})")
                else:
                    st.write(f"{t['pending']} {num}")
    else:
        st.info("👆 " + ("قم برفع ملف CSV/Excel أو أدخل الأرقام يدوياً في الشريط الجانبي" if lang == 'ar' else "Upload a CSV/Excel file or enter numbers manually in the sidebar"))

# Send button and status
st.markdown("---")
col_btn1, col_btn2, col_status = st.columns([1, 1, 2])

with col_btn1:
    send_button = st.button(
        t['send_messages'],
        type="primary",
        disabled=st.session_state.is_sending or not st.session_state.numbers_list
    )

with col_btn2:
    clear_button = st.button(
        t['clear_all'],
        disabled=st.session_state.is_sending
    )

if clear_button:
    st.session_state.numbers_list = []
    st.session_state.message_text = ""
    st.session_state.image_file = None
    st.session_state.sending_status = {}
    st.rerun()

# Status display
if st.session_state.is_sending:
    st.info(t['sending_in_progress'])

# Handle send button click
if send_button and not st.session_state.is_sending:
    if not st.session_state.numbers_list:
        st.error(t['no_numbers'])
    elif not st.session_state.message_text and not st.session_state.image_file:
        st.error(t['no_content'])
    else:
        st.session_state.is_sending = True
        st.session_state.sending_status = {num: "pending" for num in st.session_state.numbers_list}
        
        # Save image temporarily if uploaded
        image_path = None
        if st.session_state.image_file:
            # Create temp directory if it doesn't exist
            temp_dir = Path("temp_uploads")
            temp_dir.mkdir(exist_ok=True)
            
            # Save uploaded image
            image_path = temp_dir / st.session_state.image_file.name
            with open(image_path, "wb") as f:
                f.write(st.session_state.image_file.getbuffer())
        
        # Create status callback function
        def update_status(number, status):
            st.session_state.sending_status[number] = status
        
        # Start sending
        try:
            st.info(t['starting'])
            
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Call the sending function with status updates
            results = send_messages_from_ui(
                numbers=st.session_state.numbers_list,
                message=st.session_state.message_text,
                image_path=str(image_path) if image_path else None,
                status_callback=update_status,
                close_tabs=False  # Don't close tabs automatically in UI mode
            )
            
            # Update final statuses
            for num, result in results.items():
                st.session_state.sending_status[num] = "success" if result else "failed"
            
            st.session_state.is_sending = False
            progress_bar.progress(1.0)
            
            # Show final summary
            success_count = sum(1 for s in st.session_state.sending_status.values() if s == "success")
            failed_count = sum(1 for s in st.session_state.sending_status.values() if s == "failed")
            
            if failed_count == 0:
                st.success(t['completed_all'])
            else:
                st.warning(t['completed_with_errors'].format(success=success_count, failed=failed_count))
            
        except Exception as e:
            st.error(f"❌ {t['failed']} خطأ: {str(e)}" if lang == 'ar' else f"❌ {t['failed']} Error: {str(e)}")
            st.session_state.is_sending = False
            # Mark all as failed on error
            for num in st.session_state.numbers_list:
                st.session_state.sending_status[num] = "failed"
        
        finally:
            # Clean up temp image if exists
            if image_path and image_path.exists():
                try:
                    image_path.unlink()
                except:
                    pass

# Footer
st.markdown("---")
st.markdown(f"**{t['tips']}**")
st.markdown(f"- {t['tip1']}")
st.markdown(f"- {t['tip2']}")
st.markdown(f"- {t['tip3']}")
