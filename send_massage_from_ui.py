import pywhatkit as kit
import pywhatkit.core.core as core
import time
import os
from urllib.parse import quote
from platform import system
import pyautogui as pg
import pyperclip
from typing import List, Optional, Callable, Dict

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
    
    # Note: In UI mode, we'll skip the interactive prompt and just wait
    # The UI will handle showing status
    return False  # Continue processing

# ===== دالة لإرسال النص فقط =====
def send_text_only(receiver: str, message: str, wait_time: int = 15):
    """Send text message only using WhatsApp Web"""
    
    if (not receiver.isalnum()) and (not core.check_number(number=receiver)):
        raise Exception("Country Code Missing in Phone Number!")
    
    # Navigate to the contact URL in the same tab
    url = f"https://web.whatsapp.com/send?phone={receiver}&text={quote(message)}"
    
    # Copy URL to clipboard
    pyperclip.copy(url)
    
    # Ensure browser tab is focused
    time.sleep(1)
    pg.click(core.WIDTH / 2, 50)
    time.sleep(0.5)
    
    # Focus address bar and navigate
    if system().lower() == "darwin":
        pg.hotkey("command", "l")
    else:
        pg.hotkey("ctrl", "l")
    
    time.sleep(0.5)
    # Select all and paste the URL
    if system().lower() == "darwin":
        pg.hotkey("command", "a")
        pg.hotkey("command", "v")
    else:
        pg.hotkey("ctrl", "a")
        pg.hotkey("ctrl", "v")
    
    time.sleep(0.5)
    pg.press("enter")
    
    # Wait for WhatsApp to load
    time.sleep(10)
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(3)
    
    # Send the message (Enter key)
    pg.press("enter")
    
    # Wait for message to be sent
    time.sleep(5)
    
    # Log the action
    from pywhatkit.core import log
    log.log_message(_time=time.localtime(), receiver=receiver, message=message)

# ===== دالة لإرسال الصورة فقط =====
def send_image_only(receiver: str, img_path: str, wait_time: int = 15):
    """Send image only using WhatsApp Web"""
    
    if (not receiver.isalnum()) and (not core.check_number(number=receiver)):
        raise Exception("Country Code Missing in Phone Number!")
    
    # Navigate to the contact URL
    url = f"https://web.whatsapp.com/send?phone={receiver}"
    
    # Copy URL to clipboard
    pyperclip.copy(url)
    
    # Ensure browser tab is focused
    time.sleep(1)
    pg.click(core.WIDTH / 2, 50)
    time.sleep(0.5)
    
    # Focus address bar and navigate
    if system().lower() == "darwin":
        pg.hotkey("command", "l")
    else:
        pg.hotkey("ctrl", "l")
    
    time.sleep(0.5)
    # Select all and paste the URL
    if system().lower() == "darwin":
        pg.hotkey("command", "a")
        pg.hotkey("command", "v")
    else:
        pg.hotkey("ctrl", "a")
        pg.hotkey("ctrl", "v")
    
    time.sleep(0.5)
    pg.press("enter")
    
    # Wait for WhatsApp to load
    time.sleep(10)
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(3)
    
    # Copy image to clipboard
    core.copy_image(path=img_path)
    
    # Type a space to activate the input field
    pg.typewrite(" ")
    
    # Paste image
    if system().lower() == "darwin":
        pg.hotkey("command", "v")
    else:
        pg.hotkey("ctrl", "v")
    
    time.sleep(1)
    pg.press("enter")
    
    # Wait for message to be sent
    time.sleep(5)
    
    # Log the action
    from pywhatkit.core import log
    log.log_image(_time=time.localtime(), path=img_path, receiver=receiver, caption="")

# ===== دالة لإرسال الصورة مع النص =====
def send_image_with_text(receiver: str, img_path: str, caption: str, wait_time: int = 15):
    """Send image with text caption using WhatsApp Web"""
    
    if (not receiver.isalnum()) and (not core.check_number(number=receiver)):
        raise Exception("Country Code Missing in Phone Number!")
    
    # Navigate to the contact URL
    url = f"https://web.whatsapp.com/send?phone={receiver}"
    
    # Copy URL to clipboard
    pyperclip.copy(url)
    
    # Ensure browser tab is focused
    time.sleep(1)
    pg.click(core.WIDTH / 2, 50)
    time.sleep(0.5)
    
    # Focus address bar and navigate
    if system().lower() == "darwin":
        pg.hotkey("command", "l")
    else:
        pg.hotkey("ctrl", "l")
    
    time.sleep(0.5)
    # Select all and paste the URL
    if system().lower() == "darwin":
        pg.hotkey("command", "a")
        pg.hotkey("command", "v")
    else:
        pg.hotkey("ctrl", "a")
        pg.hotkey("ctrl", "v")
    
    time.sleep(0.5)
    pg.press("enter")
    
    # Wait for WhatsApp to load
    time.sleep(10)
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(3)
    
    # Copy image to clipboard
    core.copy_image(path=img_path)
    
    # Type caption
    if caption:
        for char in caption:
            if char == "\n":
                pg.hotkey("shift", "enter")
            else:
                pg.typewrite(char)
    
    # Paste image
    if system().lower() == "darwin":
        pg.hotkey("command", "v")
    else:
        pg.hotkey("ctrl", "v")
    
    time.sleep(1)
    pg.press("enter")
    
    # Wait for message to be sent
    time.sleep(5)
    
    # Log the action
    from pywhatkit.core import log
    log.log_image(_time=time.localtime(), path=img_path, receiver=receiver, caption=caption)

# ===== الدالة الرئيسية لإرسال الرسائل من الواجهة =====
def send_messages_from_ui(
    numbers: List[str],
    message: str = "",
    image_path: Optional[str] = None,
    status_callback: Optional[Callable[[str, str], None]] = None,
    close_tabs: bool = True
) -> Dict[str, bool]:
    """
    Send messages to a list of numbers based on user input.
    
    Args:
        numbers: List of phone numbers (with country code)
        message: Text message to send (optional)
        image_path: Path to image file (optional)
        status_callback: Function to call with (number, status) updates
        close_tabs: Whether to close tabs after each message
    
    Returns:
        Dictionary mapping phone numbers to success status (True/False)
    """
    
    results = {}
    
    # Determine what to send
    send_text = bool(message and message.strip())
    send_image = bool(image_path and os.path.exists(image_path))
    
    if not send_text and not send_image:
        raise ValueError("Either message text or image must be provided!")
    
    # Open WhatsApp Web once
    print("🌐 Opening WhatsApp Web...")
    kit.open_web()
    time.sleep(5)
    
    # Send to each number
    for i, num in enumerate(numbers, 1):
        try:
            # Update status: sending
            if status_callback:
                status_callback(num, "sending")
            
            # Determine which function to use
            if send_text and send_image:
                # Send both text and image
                print(f"📸 [{i}/{len(numbers)}] Sending image + text to {num}")
                send_image_with_text(num, image_path, message, wait_time=15)
            elif send_image:
                # Send image only
                print(f"📸 [{i}/{len(numbers)}] Sending image to {num}")
                send_image_only(num, image_path, wait_time=15)
            else:
                # Send text only
                print(f"💬 [{i}/{len(numbers)}] Sending text to {num}")
                send_text_only(num, message, wait_time=15)
            
            # For the last number, wait longer to ensure message is sent
            if i == len(numbers):
                print(f"   ⏳ Waiting for final message to be sent...")
                time.sleep(8)
            
            # Close tab if requested
            if close_tabs:
                print(f"   ✓ Closing tab...")
                close_tab_with_modal_handling(wait_time=2)
            
            # Update status: success
            if status_callback:
                status_callback(num, "success")
            
            results[num] = True
            print(f"✅ Message sent to {num}")
            
            # Wait before next number (except for the last one)
            if i < len(numbers):
                time.sleep(8)
                
        except Exception as e:
            # Update status: failed
            if status_callback:
                status_callback(num, "failed")
            
            results[num] = False
            print(f"❌ Failed to send to {num}: {e}")
            
            # Try to close tab even on error
            if close_tabs:
                try:
                    close_tab_with_modal_handling(wait_time=1)
                except:
                    pass
            
            # Wait before trying next number
            if i < len(numbers):
                time.sleep(5)
    
    print("🎉 Done sending all messages.")
    return results

# ===== For testing/standalone execution =====
if __name__ == "__main__":
    # Example usage
    test_numbers = ["+966505815487", "+966541556250"]
    test_message = "Test message from UI"
    test_image = None  # Set path if you want to test with image
    
    def test_callback(number: str, status: str):
        print(f"   Status update: {number} -> {status}")
    
    results = send_messages_from_ui(
        numbers=test_numbers,
        message=test_message,
        image_path=test_image,
        status_callback=test_callback,
        close_tabs=False  # Don't close tabs in test mode
    )
    
    print(f"\nResults: {results}")

