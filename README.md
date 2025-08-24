# 🕐 Shutdown Timer

A stylish system shutdown timer with terminal-like interface for Windows.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/Windows-10%2B-blue.svg)](https://microsoft.com/windows)

## 🚀 Quick Install

```bash
# Install from PyPI
pip install shutdown-timer

# Run the application
shutdown-timer
```

## 📦 Alternative Installation Methods

### From Source
```bash
# Clone the repository
git clone https://github.com/pukdev/shutdown-timer.git
cd shutdown-timer

# Install in development mode
pip install -e .

# Run directly
python shutdown_timer_embedded.py
```

### Download Executable
- Download the latest release from [Releases](https://github.com/pukdev/shutdown-timer/releases)
- Extract and run `shutdown_timer_embedded.exe`

## 🎯 Why This Project?

### The Problem
Standard Windows shutdown tools are either:
- 🥱 **Too basic** - Command line only
- 🗓️ **Visually outdated** - Windows 95 style interfaces  
- 🤯 **Feature bloated** - Unnecessary complexity with ads

### Our Solution
A **modern, elegant shutdown timer** that combines:
- 🎨 **Aesthetic appeal** - Terminal/Matrix inspired design
- ⚡ **Simplicity** - Just the features you need  
- 🌍 **Accessibility** - Native Russian and English support
- 📦 **Convenience** - Single portable executable
- 🔄 **Real-time feedback** - Live countdown display

---

## ⚡ Key Features Explained

### 🖥️ Terminal-Style Interface
- Matrix-inspired green-on-black design
- Retro computing aesthetics with modern functionality
- Dark Windows title bar integration (Windows 10/11)

### ⏰ Smart Time Management  
- **Slider control**: Quick time selection from 1 minute to 12 hours
- **Manual input**: Precise time entry for exact scheduling
- **Live countdown**: Real-time display of remaining time
- **Instant feedback**: Visual confirmation of all actions

### 🌍 Dual Language Support
- **Russian interface**: Complete localization including time formats
- **English interface**: International accessibility  
- **One-click switching**: Toggle languages instantly
- **Smart grammar**: Proper word forms for both languages

### 📦 Zero-Install Experience
- **Portable executable**: No installation required
- **Self-contained**: All dependencies included
- **Registry clean**: No system modifications
- **USB friendly**: Run from any location

---

## 🏆 What Makes This Special?

Unlike other shutdown timers, this project showcases:

### 🤖 AI-Enhanced Development
- **Human creativity** meets **AI efficiency**
- Rapid prototyping with manual refinement
- Modern development practices demonstration
- Clean, maintainable code architecture

### 🎨 Design Excellence
- **Unique aesthetic** - First shutdown timer with Matrix styling
- **User experience focus** - Intuitive without being dumbed-down
- **Visual consistency** - Every element carefully designed
- **Attention to detail** - Hover effects, animations, polish

### 💻 Technical Quality
- **Cross-compatible** - Works on Windows 10 and 11
- **System tray support** - Minimize to tray with background operation
- **Resource efficient** - Minimal memory footprint
- **Robust error handling** - Graceful failure management
- **Clean termination** - Proper process cleanup

## 🔒 Security & Privacy

### What This App Does
- ✅ **Only shutdown command** - Uses Windows built-in `shutdown` command
- ✅ **No network access** - Completely offline operation
- ✅ **No data collection** - Zero telemetry or analytics
- ✅ **No registry changes** - Leaves system untouched
- ✅ **Transparent code** - Full source available

### What This App NEVER Does
- ❌ No internet connections
- ❌ No file system modifications outside temp folder
- ❌ No personal data access
- ❌ No background processes
- ❌ No automatic updates or phone-home

### Antivirus Notes
Some antivirus may flag PyInstaller executables as suspicious - this is a known false positive. The complete source code is available for inspection.

## 📁 Project Files

### Main Applications
- `shutdown_timer_2.1.py` - **Latest version** with system tray support
- `shutdown_timer_embedded.py` - Original embedded version
- `test_tray.py` - Test application for tray functionality

### Documentation
- `TRAY_FEATURES.md` - Detailed guide for system tray features
- `requirements.txt` - Python dependencies including tray support

