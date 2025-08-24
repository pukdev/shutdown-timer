# Shutdown Timer 2.0.0

## What's New
- ✅ Standalone EXE (no Python required)
- ✅ Portable — can run from USB without installation
- ✅ HiDPI support and window centering
- ✅ RU/EN localization with dynamic text updates
- ✅ Double-start protection for timer
- ℹ️ Shutdown performed via built-in Windows `shutdown` command (WinAPI used for DPI/title bar)

## Downloads
- `ShutdownTimer_v2.exe` — main version for Windows users (recommended)
- `shutdown_timer-2.0.0-py3-none-any.whl` — package for pip installation
- `shutdown_timer-2.0.0.tar.gz` — source code (sdist)

## Usage (EXE)
1. Download `ShutdownTimer_v2.exe`
2. Run with double-click
3. Select time and press [START]
4. Use [STOP] to cancel (internally uses `shutdown /a`)

## Installation via pip (alternative)
```bash
pip install shutdown-timer
shutdown-timer
```

## Requirements
- Windows 10/11 (64-bit)
- Administrator rights for system shutdown
- ~10 MB free space

## Checksums (SHA256)
- ShutdownTimer_v2.exe: `47F25CBB36D39200CFA1F5894149DACC410B72CC9DB95D5E4B143C444AE549E5`
- shutdown_timer-2.0.0-py3-none-any.whl: `2E673DF79682D3370A48867A819567D196C16675DB69B041951368028A545442`
- shutdown_timer-2.0.0.tar.gz: `AD413019B0B4F483D5F3F713911E1AA2F4BEBD05FEDA52E5F4934CBE21BF9F8F`

## Security Notes
- Application works offline, doesn't collect data or modify registry
- EXE built with PyInstaller; some antiviruses may false-trigger on portable binaries

Author: @pukdev


