import time
import threading
import os
import sys
import winreg
import ctypes
import win32con
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import win10toast
import keyboard  # pip install keyboard

# === Globals ===
autorun_key = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
autorun_name = "CapsLangSwitcher"
settings_key = r"Software\\CapsLangSwitcher"
caps_pressed_time = None
is_caps_pressed = False
icon = None
toaster = win10toast.ToastNotifier()

# === Paths ===
def script_vbs_path():
    script = os.path.realpath(sys.argv[0])
    return os.path.splitext(script)[0] + ".vbs"

def script_exe_path():
    return os.path.realpath(sys.argv[0])

# === Settings Management ===
def is_notifications_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, settings_key, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "Notifications")
        winreg.CloseKey(key)
        return bool(val)
    except FileNotFoundError:
        return True

def set_notifications(enabled: bool):
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, settings_key)
    winreg.SetValueEx(key, "Notifications", 0, winreg.REG_DWORD, int(enabled))
    winreg.CloseKey(key)

# === Autostart Management ===
def is_autorun_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, autorun_key, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, autorun_name)
        winreg.CloseKey(key)
        return val == script_vbs_path()
    except FileNotFoundError:
        return False

def add_to_startup():
    path = script_exe_path()
    vbs = script_vbs_path()
    code = (
        'Set WshShell = CreateObject("WScript.Shell")\n'
        f'WshShell.Run chr(34) & "{path}" & chr(34), 0, False\n'
        'Set WshShell = Nothing\n'
    )
    with open(vbs, "w", encoding="utf-8") as f:
        f.write(code)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, autorun_key, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, autorun_name, 0, winreg.REG_SZ, vbs)
    winreg.CloseKey(key)
def remove_from_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, autorun_key, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, autorun_name)
        winreg.CloseKey(key)
        os.remove(script_vbs_path())
    except Exception:
        pass

# === Language Switch and CapsLock ===
def switch_language():
    ctypes.WinDLL('user32').PostMessageW(0xffff, 0x50, 1, 0)

def handle_press(event=None):
    global caps_pressed_time, is_caps_pressed
    if not is_caps_pressed:
        is_caps_pressed = True
        caps_pressed_time = time.time()


def handle_release(event=None):
    global caps_pressed_time, is_caps_pressed
    if is_caps_pressed:
        is_caps_pressed = False
        held = time.time() - caps_pressed_time
        if held < 0.2:
            # short press: switch layout
            switch_language()
            show_notification("Язык переключён")
        else:
            # long press: toggle CapsLock via keybd_event
            ctypes.windll.user32.keybd_event(0x14, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x14, 0, win32con.KEYEVENTF_KEYUP, 0)
            show_notification("CapsLock активирован")

# === Notifications ===
def show_notification(message: str):
    print(message)
    if is_notifications_enabled():
        toaster.show_toast("CapsLangSwitcher", message, duration=2, threaded=True)

# === System Tray Icon ===
def create_image(state=False):
    img = Image.new('RGB', (64, 64), color=(0, 128, 0) if not state else (128, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((16, 20), "CL", fill=(255, 255, 255))
    return img

def toggle_autorun(item):
    if is_autorun_enabled():
        remove_from_startup()
    else:
        add_to_startup()
    icon.update_menu()
    return True

def toggle_notifications(item):
    set_notifications(not is_notifications_enabled())
    icon.update_menu()
    return True

def exit_app(item):
    icon.stop()
    os._exit(0)
    return True

# === Setup Functions ===
def setup_hotkeys():
    # intercept CapsLock press/release, suppress default behavior
    keyboard.on_press_key('caps lock', lambda e: handle_press(), suppress=True)
    keyboard.on_release_key('caps lock', lambda e: handle_release(), suppress=True)


def setup_tray():
    menu = Menu(
        MenuItem("Автозагрузка", toggle_autorun, checked=lambda _: is_autorun_enabled()),
        MenuItem("Уведомления", toggle_notifications, checked=lambda _: is_notifications_enabled()),
        MenuItem("Выход", exit_app)
    )
    global icon
    icon = Icon("capslang", create_image(), "CapsLangSwitcher", menu=menu)
    def refresh_icon():
        while True:
            state = bool(ctypes.windll.user32.GetKeyState(0x14) & 0x0001)
            icon.icon = create_image(state)
            time.sleep(0.2)
    threading.Thread(target=refresh_icon, daemon=True).start()
    icon.run()

# === Main ===
if __name__ == "__main__":
    if not (len(sys.argv) > 1 and sys.argv[1] == "--no-autostart"):
        add_to_startup()
    set_notifications(is_notifications_enabled())
    setup_hotkeys()
    setup_tray()
