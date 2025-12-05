import pywhatkit as kit
import time
import os
from platform import system
import pyautogui as pg

# ===== إعداد الأرقام + المسارات =====
numbers = [
    "+966505815487",
    "+966541556250",
]

BASE_DIR = "/Users/ahmedalnemer/Desktop/Work stuff/whatsapp group massage script"
MESSAGE_FILE = os.path.join(BASE_DIR, "massage.txt")
IMAGE_PATH = os.path.join(BASE_DIR, "PHOTO-2025-12-04-20-36-25.jpg")

with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
    MESSAGE = f.read().strip()

# ===== دالة لإغلاق التاب مع إيقاف عند ظهور نافذة التأكيد =====
def close_tab_with_modal_handling(wait_time: int = 2) -> bool:
    """Closes the Currently Opened Browser Tab and stops if WhatsApp modal dialog appears.
    Returns True if modal was detected and user wants to stop, False otherwise."""
    
    time.sleep(wait_time)
    
    # Close the tab using keyboard shortcut
    if system().lower() in ("windows", "linux"):
        pg.hotkey("ctrl", "w")
    elif system().lower() == "darwin":
        pg.hotkey("command", "w")
    else:
        raise Warning(f"{system().lower()} not supported!")
    
    # Wait a moment - if another tab is open, WhatsApp will show a modal
    # If no other tab is open, the tab will just close
    time.sleep(2)
    
    # Stop execution when modal might appear - always pause to let user handle it
    # The modal shows: "واتساب مفتوح في نافذة أخرى. انقر على "الاستخدام هنا" لاستخدام واتساب في هذه النافذة."
    print("\n" + "="*70)
    print("⚠️  STOPPED: Close confirmation dialog detected or may have appeared!")
    print("   A WhatsApp modal may be asking about closing the tab.")
    print("   Please check your browser and handle the dialog:")
    print("   - Click 'إغلاق' (Close) to confirm closing the tab")
    print("   - Or click 'الاستخدام هنا' (Use here) to keep using this window")
    print("="*70)
    print("\n⏸️  Script stopped. What would you like to do?")
    print("   [c] Continue processing remaining numbers")
    print("   [s] Stop script completely (exit)")
    print("   [Enter] Continue (default)")
    
    # Wait for user input
    user_choice = input("\n   Your choice: ").strip().lower()
    
    if user_choice == 's':
        print("\n🛑 Script stopped by user.")
        return True  # Signal to stop processing
    else:
        print("✓ Continuing...\n")
        return False  # Continue processing

# ===== حلقة الإرسال =====
for i, num in enumerate(numbers, 1):
    try:
        print(f"📸 [{i}/{len(numbers)}] Sending image + caption to {num}")
        
        # Send the image (without closing the tab automatically)
        kit.sendwhats_image(num, IMAGE_PATH, caption=MESSAGE, wait_time=15, tab_close=False)
        
        # For the last number, wait longer to ensure message is sent before closing
        if i == len(numbers):
            print("   ⏳ Waiting for final message to be sent...")
            time.sleep(8)  # Extra wait time for the last message
            print("   ✓ Closing tab...")
            # Use our custom close function that handles the modal
            should_stop = close_tab_with_modal_handling(wait_time=2)
            if should_stop:
                print("\n🛑 Script stopped. Exiting...")
                break
        else:
            # For other numbers, close the tab normally
            print("   ✓ Closing tab...")
            should_stop = close_tab_with_modal_handling(wait_time=2)
            if should_stop:
                print(f"\n🛑 Script stopped. {len(numbers) - i} number(s) remaining.")
                break
            time.sleep(5)  # أترك بعض وقت قبل الرقم التالي
        
        print(f"✅ Image sent to {num} (and tab closed).")
    except Exception as e:
        print(f"❌ Failed for {num}: {e}")
        # Try to close the tab even if there was an error
        try:
            should_stop = close_tab_with_modal_handling(wait_time=1)
            if should_stop:
                print("\n🛑 Script stopped due to error. Exiting...")
                break
        except:
            pass

print("🎉 Done.")

