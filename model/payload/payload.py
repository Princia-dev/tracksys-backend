# payload/payload.py
import pyautogui
import datetime

def capture_ecran():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshot_{timestamp}.png")

if __name__ == "__main__":
    capture_ecran()