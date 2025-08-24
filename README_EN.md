# Shutdown Timer

A stylish system shutdown timer with terminal-style interface.

**[🇷🇺 Russian version](README.md)**

## 🚀 Quick Installation

### Download Ready EXE (recommended)
**[📥 Download ShutdownTimer_v2.exe](https://github.com/pukdev/shutdown-timer/releases/download/v2.0.0/ShutdownTimer_v2.exe)** (10.0 MB)

Just download and run — no Python required!

### Install via pip
```bash
pip install shutdown-timer
shutdown-timer
```

## Alternative Installation Methods

### From Source Code
```bash
git clone https://github.com/pukdev/shutdown-timer.git
cd shutdown-timer
pip install -e .
shutdown-timer
```

### Download Executable
- Download `ShutdownTimer_v2.exe` from [releases](https://github.com/pukdev/shutdown-timer/releases/latest)
- Run the file directly (no Python installation required)
- **SHA256:** `47F25CBB36D39200CFA1F5894149DACC410B72CC9DB95D5E4B143C444AE549E5`

## Compiling EXE

To create an executable file:

```bash
# Install PyInstaller
pip install pyinstaller

# Compile EXE
pyinstaller --onefile --windowed --icon=terminal_icon_2.ico --name="ShutdownTimer" shutdown_timer_embedded.py
```

The ready EXE file will be in the `dist/` folder.

## ✨ Features

- ⏰ Shutdown timer with countdown
- 🎨 Modern terminal-style interface
- 🌍 Russian and English language support
- 🖥️ HiDPI support for high resolution
- 🛡️ Double-start protection
- ⚡ Fast launch and cancellation
- 📦 Standalone EXE (no Python required)
- 🔒 Security — works offline, doesn't collect data

## Usage

1. Launch the application
2. Select shutdown time (from 1 minute to 24 hours)
3. Press "Start Timer"
4. Use "Cancel Shutdown" to stop

## System Requirements

- Windows 10/11 (64-bit)
- Python 3.7+ (only for pip installation)
- Administrator rights for system shutdown
- ~10 MB free space

## License

MIT License - see [LICENSE](LICENSE) file

## Author

[pukdev](https://github.com/pukdev)

## 📋 Versions

- **v2.0.0** — Current version with standalone EXE
- [Full changelog](https://github.com/pukdev/shutdown-timer/releases)

## 🆘 Support

If you have questions or suggestions, create an [issue](https://github.com/pukdev/shutdown-timer/issues) on GitHub.
