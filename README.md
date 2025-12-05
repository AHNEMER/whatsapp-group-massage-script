# WhatsApp Message Sender - Web UI

A Streamlit web application for sending WhatsApp messages to multiple recipients with support for text messages, images, or both.

## Features

- 📤 **Upload CSV/Excel/Apple Numbers files** with phone numbers (auto-detects phone columns)
- 📝 **Type messages** directly in the UI
- 🖼️ **Upload images** to send with messages (with preview)
- 📋 **Scrollable list** of phone numbers with live status updates
- ✅ **Real-time status** showing which numbers messages were sent to successfully
- 🔄 **Automatic handling** of text-only, image-only, or both
- 🌐 **Arabic/English language support** (Arabic as default)
- 📱 **Smart phone number normalization** (966→+966, 05→+9665, etc.)
- ⚠️ **Warning system** to ensure WhatsApp tabs are closed before starting

## Installation

1. Install required packages:
```bash
pip install -r requirements_ui.txt
```

**Note:** For Apple Numbers (.numbers) file support, the `numbers-parser` library is required and will be installed automatically with the requirements.

## Usage

1. Start the Streamlit app:
```bash
streamlit run ui_app.py
```

2. The app will open in your browser (usually at `http://localhost:8501`)

3. **Upload phone numbers:**
   - Upload a CSV/Excel file with phone numbers in a column
   - Or enter numbers manually in the sidebar (one per line)
   - Numbers must include country code (e.g., +966505815487)

4. **Enter message content:**
   - Type your message in the text area
   - Optionally upload an image
   - You can send:
     - Text only
     - Image only
     - Both text and image

5. **Send messages:**
   - Click "🚀 Send Messages" button
   - Watch the live feed as messages are sent
   - Status will update in real-time:
     - ⏸️ Pending
     - ⏳ Sending
     - ✅ Success
     - ❌ Failed

## File Format Support

The app supports the following file formats:
- **CSV** (.csv)
- **Excel** (.xlsx, .xls)
- **Apple Numbers** (.numbers)

Your file should contain phone numbers in a column. The app will automatically detect columns with names containing:
- phone, Phone
- number
- phone number
- ext
- mobile, tel, whatsapp

If no matching column is found, it will use the first column.

### Phone Number Formats Supported

The app automatically normalizes phone numbers:
- `966505815487` → `+966505815487`
- `0551234567` → `+966551234567`
- `+966505815487` → `+966505815487` (already correct)

Example CSV:
```csv
phone
966505815487
0551234567
+966541556250
```

## Notes

- ⚠️ **IMPORTANT**: Close all WhatsApp Web tabs before starting to send messages
- Make sure **WhatsApp Web is logged in** before sending messages
- The app will reuse the same browser tab for all messages
- Phone numbers are automatically normalized (966→+966, 05→+9665)
- The app supports Arabic and English languages (switch in sidebar)
- The app will not automatically close tabs (unlike the original script)

## Troubleshooting

- If messages fail to send, check that WhatsApp Web is open and logged in
- Ensure phone numbers are in the correct format with country code
- Make sure you have a stable internet connection

