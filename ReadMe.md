# CapsLock Language Toggle

A lightweight Windows tray application that turns your Caps Lock key into a powerful language switcher and true Caps Lock toggle.

## Project Name

**CapsLock Language Toggle** – crystal clear: short, descriptive, and instantly tells you this app toggles input language and Caps Lock behavior.

## Features

* **Short press on Caps Lock**: instantly switch input language (e.g., between English and Russian).
* **Long press on Caps Lock**: behave like normal Caps Lock (toggle uppercase mode).
* **Tray icon**: shows current Caps Lock state (green = off, red = on).
* **System notifications**: optional pop-ups when switching modes (can be disabled).
* **Auto-start**: add or remove itself from Windows startup via tray menu.
* **Silent background mode**: no console window pops up at launch.

## Installation

1. Clone or download the repository.
2. Ensure you have Python 3.8+ installed.
3. Install dependencies with pip:

   ```bash
   pip install pystray pynput pillow win10toast keyboard pywin32
   ```
4. (Optional) Rename `main.py` to `capslock_toggle.pyw` to hide the console window.

## Usage

1. Run the script:

   ```bash
   python capslock_toggle.pyw
   ```
2. A tray icon labeled **CL** will appear near your clock.
3. Right-click the icon to access the menu:

   * **Автозагрузка** – toggle auto-start on Windows login.
   * **Уведомления** – enable/disable pop-up notifications.
   * **Выход** – quit the application.
4. Use the Caps Lock key:

   * **Short tap (<0.2s)**: switch keyboard layout.
   * **Long press (>=0.2s)**: toggle uppercase mode.

## Configuration

Settings are stored in the Windows registry under:

```
HKEY_CURRENT_USER\Software\CapsLangSwitcher
```

* `Notifications` (DWORD): `1` = enabled, `0` = disabled.

## License

MIT License – feel free to use, modify, and distribute.
