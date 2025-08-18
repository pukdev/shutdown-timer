# 🚀 Инструкция по сборке оптимизированной версии

## Требования
- Windows 10/11
- Python 3.8+ (скачать с python.org)

## Пошаговая сборка

### 1. Установи PyInstaller
```bash
pip install pyinstaller
```

### 2. Скачай файлы проекта
- `shutdown_timer_embedded.py` (оптимизированная версия)
- `terminal_icon_2.ico` (иконка)

### 3. Собери исполняемый файл
```bash
pyinstaller --noconsole --onefile --add-data "terminal_icon_2.ico;." --name "shutdown_timer_optimized" shutdown_timer_embedded.py
```

### 4. Готово! 
Файл будет в папке `dist/shutdown_timer_optimized.exe`

## 📊 Результат оптимизации
- ✅ Быстрый старт (без декодирования base64)
- ✅ Стабильный countdown (без потоков)
- ✅ Меньше памяти (файловая иконка)
- ✅ Чистое завершение (корректная отмена таймеров)

## 🔧 Альтернатива: оригинальная версия
Если нужна старая версия с встроенной иконкой:
```bash
pyinstaller --noconsole --onefile shutdown_timer_2.0.py
```

## 🐛 Если антивирус ругается
Это ложное срабатывание на PyInstaller. Исходный код открыт для проверки.