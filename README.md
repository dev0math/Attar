# Attar

A lightweight Islamic dhikr reminder for Linux. Runs quietly in the background and displays elegant notification cards with random adhkar at configurable intervals.

---

## Features

- Animated notification cards with smooth slide-in and fade transitions
- Full Arabic UI with light and dark themes
- Select which adhkar appear in reminders
- Configurable reminder interval (1–120 minutes)
- Adjustable notification duration and screen position
- Daily and total reminder statistics
- Optional autostart on system boot

---

## Requirements

| Dependency | Version |
|---|---|
| Python | 3.10+ |
| PyQt6 | 6.x |

**Debian / Ubuntu**
```bash
sudo apt install python3 python3-pyqt6
```

**Arch Linux**
```bash
sudo pacman -S python python-pyqt6
```

**Fedora**
```bash
sudo dnf install python3 python3-pyqt6
```

---

## Installation

```bash
git clone https://github.com/dev0math/Attar
cd Attar
bash install.sh
```

---

## Usage

```bash
attar --gui          # Open the graphical control panel
attar --start        # Start the background daemon
attar --stop         # Stop the daemon
attar --status       # Show current daemon status
attar --version      # Print version
attar --uninstall    # Uninstall Attar
```

---

## Project Structure

```
attar/
├── attar/
│   ├── __init__.py
│   ├── config.py        # Settings management
│   ├── daemon.py        # Background process
│   ├── dhikr.py         # Adhkar data
│   ├── gui.py           # Graphical interface
│   ├── notifier.py      # Notification card
│   ├── themes.py        # Light and dark themes
│   └── assets/
│       └── icon.svg
├── install.sh
├── uninstall.sh
└── README.md
```

---

## Uninstall

```bash
bash uninstall.sh
# or
attar --uninstall
```

---

## Contributing

If you encounter a bug or a security vulnerability, please open an issue. Every report helps improve the project, and sharing knowledge benefits us all. Your time and attention are appreciated.

---

## License

MIT — Built with care by [DEV](https://github.com/dev0math)
