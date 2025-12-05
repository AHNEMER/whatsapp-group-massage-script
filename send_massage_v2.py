import pywhatkit as kit
import pywhatkit.core.core as core
import time
import os
from urllib.parse import quote
from platform import system
import pyautogui as pg
import pyperclip

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

# ===== دالة مخصصة لإرسال الصورة باستخدام نفس التاب =====
def send_image_same_tab(receiver: str, img_path: str, caption: str = "", wait_time: int = 15):
    """Send Image using the same WhatsApp Web tab by navigating to the contact URL"""
    
    if (not receiver.isalnum()) and (not core.check_number(number=receiver)):
        raise Exception("Country Code Missing in Phone Number!")
    
    # Navigate to the contact URL in the same tab
    url = f"https://web.whatsapp.com/send?phone={receiver}&text={quote(caption)}"
    
    # Copy URL to clipboard
    pyperclip.copy(url)
    
    # Ensure browser tab is focused (click on it first)
    time.sleep(1)
    pg.click(core.WIDTH / 2, 50)  # Click near top of screen to focus browser
    time.sleep(0.5)
    
    # Focus address bar and navigate (Cmd+L on Mac, Ctrl+L on Windows/Linux)
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
    
    # Wait for WhatsApp to load and navigate to the contact
    print(f"   ⏳ Navigating to {receiver}...")
    time.sleep(10)  # Increased wait time for page navigation
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(3)  # Additional wait to ensure chat is ready
    print(f"   ✓ Chat ready for {receiver}")
    
    # Copy image to clipboard
    core.copy_image(path=img_path)
    
    # Type caption if needed
    if core.check_number(number=receiver):
        pg.typewrite(" ")
    else:
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
    
    # Wait for message to be sent (check for sent indicator)
    print(f"   ⏳ Waiting for message to be sent to {receiver}...")
    time.sleep(5)  # Wait for message to be sent before moving to next contact
    
    # Log the action
    from pywhatkit.core import log
    log.log_image(_time=time.localtime(), path=img_path, receiver=receiver, caption=caption)

# ===== فتح WhatsApp Web مرة واحدة فقط =====
print("🌐 Opening WhatsApp Web (this will be reused for all messages)...")
kit.open_web()
time.sleep(5)  # Wait for WhatsApp Web to load initially

# ===== حلقة الإرسال =====
for i, num in enumerate(numbers, 1):
    try:
        print(f"📸 [{i}/{len(numbers)}] Sending image + caption to {num}")
        send_image_same_tab(num, IMAGE_PATH, caption=MESSAGE, wait_time=15)
        print(f"✅ Image sent to {num}.")
        if i < len(numbers):  # Don't wait after the last message
            print("⏳ Waiting before next contact...")
            time.sleep(8)  # Increased wait time between contacts
    except Exception as e:
        print(f"❌ Failed for {num}: {e}")
        print("⏳ Waiting before trying next contact...")
        time.sleep(5)

print("🎉 Done. You can close the WhatsApp Web tab manually when finished.")

