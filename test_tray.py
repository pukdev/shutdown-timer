#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый файл для проверки работы системного трея
"""

import tkinter as tk
from tkinter import messagebox

# Проверяем доступность pystray
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
    print("✓ pystray доступен")
except ImportError as e:
    TRAY_AVAILABLE = False
    print(f"✗ pystray недоступен: {e}")

def create_tray_icon():
    """Создает иконку для системного трея"""
    if not TRAY_AVAILABLE:
        return None
    
    # Создаем простую иконку
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Рисуем простую иконку таймера
    draw.ellipse([8, 8, 56, 56], fill=(0, 255, 65, 255), outline=(0, 255, 0, 255), width=2)
    draw.line([32, 32, 32, 16], fill=(0, 0, 0, 255), width=2)  # часовая стрелка
    draw.line([32, 32, 44, 32], fill=(0, 0, 0, 255), width=2)  # минутная стрелка
    
    return image

class TestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тест системного трея")
        self.geometry("300x200")
        self.resizable(False, False)
        
        # Переменная для иконки трея
        self.tray_icon = None
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Инициализация трея
        self.setup_tray()
        
        # Обработчик закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        """Создает элементы интерфейса"""
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True, fill="both")
        
        # Заголовок
        title = tk.Label(frame, text="Тест системного трея", font=("Arial", 14, "bold"))
        title.pack(pady=(0, 20))
        
        # Информация о доступности
        status_text = "✓ Системный трей доступен" if TRAY_AVAILABLE else "✗ Системный трей недоступен"
        status = tk.Label(frame, text=status_text, fg="green" if TRAY_AVAILABLE else "red")
        status.pack(pady=(0, 20))
        
        # Инструкции
        instructions = tk.Label(frame, text="Нажмите на крестик, чтобы свернуть в трей\nПравый клик на иконке трея для меню", 
                               justify="center")
        instructions.pack(pady=(0, 20))
        
        # Кнопка для тестирования
        test_btn = tk.Button(frame, text="Показать сообщение", command=self.show_message)
        test_btn.pack()
    
    def setup_tray(self):
        """Настраивает иконку в системном трее"""
        if not TRAY_AVAILABLE:
            return
        
        try:
            image = create_tray_icon()
            menu = self.create_tray_menu()
            self.tray_icon = pystray.Icon("test_timer", image, "Тест таймера", menu)
            self.tray_icon.run_detached()
            print("✓ Иконка трея создана")
        except Exception as e:
            print(f"✗ Ошибка создания иконки трея: {e}")
    
    def create_tray_menu(self):
        """Создает меню для иконки трея"""
        if not TRAY_AVAILABLE:
            return None
        
        def show_window():
            """Показывает окно программы"""
            self.deiconify()
            self.lift()
            self.focus_force()
            print("✓ Окно показано")

        def quit_app():
            """Полностью закрывает приложение"""
            print("✓ Приложение закрывается")
            if self.tray_icon:
                self.tray_icon.stop()
            self.quit()

        menu = pystray.Menu(
            pystray.MenuItem("Показать", show_window),
            pystray.MenuItem("Выход", quit_app)
        )
        return menu
    
    def show_message(self):
        """Показывает тестовое сообщение"""
        messagebox.showinfo("Тест", "Системный трей работает!")
    
    def on_close(self):
        """Обработчик закрытия окна"""
        if TRAY_AVAILABLE and self.tray_icon:
            print("✓ Окно сворачивается в трей")
            self.withdraw()  # Скрываем окно в трей
        else:
            print("✓ Окно закрывается")
            self.destroy()

if __name__ == "__main__":
    print("Запуск теста системного трея...")
    app = TestApp()
    app.mainloop()

