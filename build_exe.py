#!/usr/bin/env python3
"""
Скрипт для компиляции Shutdown Timer в EXE файл
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Выполняет команду и выводит результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} завершено успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description}:")
        print(f"   Команда: {cmd}")
        print(f"   Ошибка: {e.stderr}")
        return False

def main():
    print("🚀 Начинаем компиляцию Shutdown Timer...")
    
    # Проверяем наличие PyInstaller
    if not run_command("pip show pyinstaller", "Проверка PyInstaller"):
        print("📦 Устанавливаем PyInstaller...")
        if not run_command("pip install pyinstaller", "Установка PyInstaller"):
            print("❌ Не удалось установить PyInstaller")
            return False
    
    # Очищаем предыдущие сборки
    print("🧹 Очищаем предыдущие сборки...")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            try:
                import shutil
                shutil.rmtree(folder)
                print(f"✅ Папка {folder} очищена")
            except PermissionError:
                print(f"⚠️  Папка {folder} используется, пропускаем очистку")
            except Exception as e:
                print(f"⚠️  Не удалось очистить {folder}: {e}")
    
    # Компилируем EXE
    cmd = 'pyinstaller --onefile --windowed --icon=terminal_icon_2.ico --name="ShutdownTimer" shutdown_timer_embedded.py'
    if not run_command(cmd, "Компиляция EXE файла"):
        return False
    
    # Проверяем результат
    exe_path = os.path.join("dist", "ShutdownTimer.exe")
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"🎉 Компиляция завершена успешно!")
        print(f"📁 Файл: {exe_path}")
        print(f"📏 Размер: {size:.1f} MB")
        print(f"🚀 Для запуска: {exe_path}")
        return True
    else:
        print("❌ EXE файл не найден после компиляции")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
