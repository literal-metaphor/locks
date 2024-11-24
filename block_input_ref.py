# * Reference code for whitelisting key press

from pynput import keyboard
from ctypes import windll

allowed_keys = {
    keyboard.Key.enter,
    keyboard.Key.space,
    keyboard.Key.backspace,
    keyboard.Key.tab,
}

def is_allowed(key):
    return key in allowed_keys or (hasattr(key, 'char') and key.char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_')

def on_press(key):
    if not is_allowed(key):
        windll.user32.BlockInput(True)
        print(f"Blocked input for key: {key}")

def on_release(key):
    windll.user32.BlockInput(False)

# Start the keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
