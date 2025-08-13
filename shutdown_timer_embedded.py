import os
import sys
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

ICON_NAME = "terminal_icon_2.ico"


def resource_path(relative_path: str) -> str:
	try:
		base_path = sys._MEIPASS  # type: ignore[attr-defined]
	except Exception:
		base_path = os.path.abspath(os.path.dirname(__file__))
	return os.path.join(base_path, relative_path)


# Цветовая тема
BG = "#0C0C0C"
CARD_BG = "#161616"
TEXT = "#00FF41"
TEXT_DIM = "#00AA2E"
TEXT_BRIGHT = "#00FF00"
BORDER = "#333333"
BTN_BG = "#1E1E1E"
BTN_HOVER = "#2A2A2A"
SLIDER_TRACK = "#333333"
SLIDER_FILL = "#00FF41"
SLIDER_THUMB = "#00FF00"
TITLE_BAR = "#1A1A1A"
INPUT_BG = "#2A2A2A"
INPUT_FG = "#00FF41"

# Локализация
current_language = "ru"
TRANSLATIONS = {
	"ru": {
		"title": "Таймер выключения системы",
		"header": "┌──── ТАЙМЕР ВЫКЛЮЧЕНИЯ СИСТЕМЫ ────┐",
		"subtitle": "│     Установите задержку до выключения     │",
		"footer": "└─────────────────────────────────────────┘",
		"command_prompt": "C:\\> SELECTOR_VREMENI.EXE --диапазон 1-720",
		"status_ready": "Статус: ГОТОВ | Диапазон: 1 мин - 12 часов",
		"status_scheduled": "Статус: ВЫКЛЮЧЕНИЕ ЗАПЛАНИРОВАНО НА",
		"status_cancelled": "Статус: ВЫКЛЮЧЕНИЕ ОТМЕНЕНО",
		"status_countdown": "Статус: ОБРАТНЫЙ ОТСЧЕТ | Осталось:",
		"btn_start": "[ СТАРТ ]",
		"btn_stop": "[ СТОП ]",
		"btn_show_manual": "[ПОКАЗАТЬ РУЧНОЙ ВВОД]",
		"btn_hide_manual": "[СКРЫТЬ РУЧНОЙ ВВОД]",
		"manual_label": "Ручной ввод (1-720 мин):",
		"btn_apply_start": "Применить",
		"error_title": "СИСТЕМНАЯ ОШИБКА",
		"error_invalid_time": "Некорректный параметр времени!",
		"error_title_input": "ОШИБКА",
		"error_range": "Значение должно быть от",
		"error_number": "Введите корректное число",
		"timer_set_title": "ТАЙМЕР ВЫКЛЮЧЕНИЯ",
		"timer_set_msg": "Система выключится через",
		"operation_title": "ОПЕРАЦИЯ",
		"operation_cancelled": "Таймер выключения отменен.",
		"language_btn": "EN",
		"shutdown_now": "СИСТЕМА ВЫКЛЮЧАЕТСЯ!",
	},
	"en": {
		"title": "System Shutdown Timer",
		"header": "┌──── SHUTDOWN TIMER MODULE ────┐",
		"subtitle": "│   Set automatic shutdown delay   │",
		"footer": "└─────────────────────────────────┘",
		"command_prompt": "C:\\> TIME_SELECTOR.EXE --range 1-720",
		"status_ready": "Status: READY | Range: 1 min - 12 hours",
		"status_scheduled": "Status: SHUTDOWN SCHEDULED FOR",
		"status_cancelled": "Status: SHUTDOWN CANCELLED",
		"status_countdown": "Status: COUNTDOWN ACTIVE | Remaining:",
		"btn_start": "[ START ]",
		"btn_stop": "[ STOP ]",
		"btn_show_manual": "[SHOW MANUAL INPUT]",
		"btn_hide_manual": "[HIDE MANUAL INPUT]",
		"manual_label": "Manual input (1-720 min):",
		"btn_apply_start": "Apply",
		"error_title": "SYSTEM ERROR",
		"error_invalid_time": "Invalid time parameter!",
		"error_title_input": "ERROR",
		"error_range": "Value must be between",
		"error_number": "Please enter a valid number",
		"timer_set_title": "SHUTDOWN TIMER",
		"timer_set_msg": "System will shutdown in",
		"operation_title": "OPERATION",
		"operation_cancelled": "Shutdown timer cancelled.",
		"language_btn": "РУ",
		"shutdown_now": "SYSTEM SHUTTING DOWN!",
	},
}


def get_text(key: str) -> str:
	return TRANSLATIONS[current_language][key]


def load_icon() -> str | None:
	path = resource_path(ICON_NAME)
	return path if os.path.exists(path) else None


def format_time(m: int) -> str:
	if current_language == "ru":
		if m < 60:
			return f">>> {m:02d} МИНУТ <<<"
		return f">>> {m//60} ЧАСОВ {m%60} МИНУТ <<<"
	else:
		if m < 60:
			return f">>> {m:02d} MINUTES <<<"
		return f">>> {m//60} HOURS {m%60} MINUTES <<<"


def format_count(sec: int) -> str:
	if sec <= 0:
		return get_text("shutdown_now")
	h = sec // 3600
	m = (sec % 3600) // 60
	s = sec % 60
	parts: list[str] = []
	if h:
		parts.append(f"{h} " + ("ЧАС" if current_language == "ru" and h == 1 else "ЧАСОВ"))
	if m:
		parts.append(f"{m} " + ("МИНУТА" if current_language == "ru" and m == 1 else "МИНУТ"))
	parts.append(f"{s} " + ("СЕКУНДА" if current_language == "ru" and s == 1 else "СЕКУНД"))
	return ">>> " + " ".join(parts) + " <<<"


# State
countdown = False
countdown_job: str | None = None
target_time: datetime | None = None


# UI
root = tk.Tk()
root.title(get_text("title"))
icon = load_icon()
if icon:
	try:
		root.iconbitmap(icon)
	except Exception:
		pass
root.configure(bg=BG)
root.geometry("540x420")
root.resizable(True, True)


def on_close():
	global countdown, countdown_job
	countdown = False
	try:
		os.system("shutdown /a")
	except Exception:
		pass
	if countdown_job:
		try:
			root.after_cancel(countdown_job)
		except Exception:
			pass
	root.destroy()
	sys.exit(0)


root.protocol("WM_DELETE_WINDOW", on_close)

try:
	import ctypes

	def dark_title(w):
		DWMWA_USE_IMMERSIVE_DARK_MODE = 20
		hwnd = ctypes.windll.user32.GetParent(w.winfo_id())
		val = ctypes.c_int(2)
		ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(val), ctypes.sizeof(val))

	root.after(100, lambda: dark_title(root))
except Exception:
	pass

MONO_NORMAL = ("Consolas", 11)
MONO_BIG = ("Consolas", 18, "bold")
MONO_SMALL = ("Courier", 8)

bar = tk.Frame(root, bg=TITLE_BAR, height=28)
bar.pack(fill="x")
tk.Label(bar, text="⬛", bg=TITLE_BAR, fg=TEXT, font=("Consolas", 10)).pack(side="left", padx=6)
tk.Label(bar, text="shutdown_timer.exe", bg=TITLE_BAR, fg=TEXT, font=("Consolas", 9)).pack(side="left")


def toggle_lang(_=None):
	global current_language
	current_language = "en" if current_language == "ru" else "ru"
	rebuild_texts()
	root.title(get_text("title"))


lang_btn = tk.Label(bar, text=get_text("language_btn"), bg=TITLE_BAR, fg=TEXT_BRIGHT, font=("Consolas", 9, "bold"), cursor="hand2")
lang_btn.pack(side="right", padx=10)
lang_btn.bind("<Button-1>", toggle_lang)
tk.Frame(root, bg=BORDER, height=1).pack(fill="x")

mf = tk.Frame(root, bg=BG)
mf.pack(fill="both", expand=True, padx=4, pady=4)
tk.Label(mf, text="C:\\Windows\\System32>", bg=BG, fg=TEXT, font=MONO_NORMAL).pack(anchor="w", padx=12, pady=(8, 4))

header = tk.Label(mf, text=get_text("header"), bg=BG, fg=TEXT_BRIGHT, font=MONO_NORMAL)
header.pack()
subtitle = tk.Label(mf, text=get_text("subtitle"), bg=BG, fg=TEXT_DIM, font=MONO_NORMAL)
subtitle.pack()
footer = tk.Label(mf, text=get_text("footer"), bg=BG, fg=TEXT_BRIGHT, font=MONO_NORMAL)
footer.pack(pady=(0, 8))

display = tk.Label(mf, text=format_time(30), bg=BG, fg=TEXT_BRIGHT, font=MONO_BIG)
display.pack()
countdown_label = tk.Label(mf, text="", bg=BG, fg="#FF6B6B", font=("Consolas", 16, "bold"))
countdown_label.pack(pady=(0, 8))

tf = tk.Frame(mf, bg=CARD_BG, relief="solid", bd=1, highlightbackground=BORDER)
tf.pack(fill="x", padx=16, pady=(0, 8))
tk.Label(tf, text=get_text("command_prompt"), bg=CARD_BG, fg=TEXT, font=MONO_SMALL).pack(anchor="w", padx=6, pady=(4, 2))
canvas = tk.Canvas(tf, bg=CARD_BG, highlightthickness=0, bd=0, height=24)
canvas.pack(fill="x", padx=6)

SL_MIN, SL_MAX = 1, 720
val = tk.IntVar(value=30)


def draw_slider():
	canvas.delete("all")
	w = canvas.winfo_width()
	if w < 2:
		root.after(50, draw_slider)
		return
	m = 12
	tw = w - 2 * m
	ty = 12
	th = 3
	ts = 10
	prog = (val.get() - SL_MIN) / (SL_MAX - SL_MIN)
	fx = m + prog * tw
	canvas.create_rectangle(m, ty - th // 2, m + tw, ty + th // 2, fill=SLIDER_TRACK, outline="")
	canvas.create_rectangle(m, ty - th // 2, m + prog * tw, ty + th // 2, fill=SLIDER_FILL, outline="")
	canvas.create_rectangle(fx - ts // 2, ty - ts // 2, fx + ts // 2, ty + ts // 2, fill=SLIDER_THUMB, outline=TEXT_BRIGHT, width=1)


root.after(100, draw_slider)


def set_val(e):
	if countdown:
		return
	w = canvas.winfo_width()
	m = 12
	tw = w - 2 * m
	p = max(0, min(1, (e.x - m) / tw))
	v = int(SL_MIN + p * (SL_MAX - SL_MIN))
	val.set(v)
	display.config(text=format_time(v))
	draw_slider()


canvas.bind("<Button-1>", set_val)
canvas.bind("<B1-Motion>", set_val)

manual_frame = tk.Frame(tf, bg=CARD_BG)
show_manual = tk.BooleanVar(value=False)


def toggle_manual():
	if countdown:
		return
	if not show_manual.get():
		show_manual.set(True)
		manual_frame.pack(fill="x", padx=6, pady=3)
		toggle_btn.config(text=get_text("btn_hide_manual"))
		entry.delete(0, "end")
		entry.insert(0, str(val.get()))
		entry.focus()
	else:
		show_manual.set(False)
		manual_frame.pack_forget()
		toggle_btn.config(text=get_text("btn_show_manual"))


toggle_btn = tk.Button(
	tf,
	text=get_text("btn_show_manual"),
	command=toggle_manual,
	bg=BTN_BG,
	fg=TEXT,
	font=MONO_SMALL,
	activebackground=BTN_HOVER,
	activeforeground=TEXT_BRIGHT,
	bd=1,
	relief="solid",
	cursor="hand2",
)

toggle_btn.pack(pady=(0, 3))

tk.Label(manual_frame, text=get_text("manual_label"), bg=CARD_BG, fg=TEXT_DIM, font=MONO_SMALL).pack(anchor="w")
row = tk.Frame(manual_frame, bg=CARD_BG)
row.pack(fill="x", pady=(2, 0))
entry = tk.Entry(row, bg=INPUT_BG, fg=INPUT_FG, font=MONO_NORMAL, insertbackground=INPUT_FG, width=8)
entry.pack(side="left", padx=(0, 6))


def apply_start():
	if countdown:
		return
	try:
		v = int(entry.get())
		if SL_MIN <= v <= SL_MAX:
			val.set(v)
			display.config(text=format_time(v))
			draw_slider()
		else:
			messagebox.showerror(get_text("error_title_input"), f"{get_text('error_range')} {SL_MIN} до {SL_MAX}")
	except Exception:
		messagebox.showerror(get_text("error_title_input"), get_text("error_number"))


entry.bind("<Return>", lambda e: apply_start())
apply_btn = tk.Button(row, text=get_text("btn_apply_start"), command=apply_start, bg=BTN_BG, fg=TEXT, font=MONO_SMALL, activebackground=BTN_HOVER, activeforeground=TEXT_BRIGHT, bd=1, relief="solid", padx=6)
apply_btn.pack(side="left")

status_label = tk.Label(tf, text=get_text("status_ready"), bg=CARD_BG, fg=TEXT_DIM, font=MONO_SMALL)
status_label.pack(anchor="w", padx=6, pady=(3, 4))
buttons = tk.Frame(mf, bg=BG)
buttons.pack(fill="x", pady=6)


def tick():
	global countdown, countdown_job
	if not countdown:
		countdown_job = None
		return
	assert target_time is not None
	rem = int((target_time - datetime.now()).total_seconds())
	text = format_count(rem)
	status = f"{get_text('status_countdown')} {text.replace('>>> ', '').replace(' <<<', '')}"
	countdown_label.config(text=text)
	status_label.config(text=status, fg="#FF6B6B")
	if rem <= 0:
		countdown = False
		countdown_job = None
		return
	countdown_job = root.after(1000, tick)


def start_shutdown():
	global countdown, target_time, countdown_job
	if countdown:
		return
	m = val.get()
	if m <= 0:
		messagebox.showerror(get_text("error_title"), get_text("error_invalid_time"))
		return
	sec = m * 60
	os.system(f"shutdown /s /t {sec}")
	countdown = True
	target_time = datetime.now() + timedelta(seconds=sec)
	countdown_job = root.after(1000, tick)
	for w in (toggle_btn, apply_btn, b_start):
		w.config(state="disabled")
	messagebox.showinfo(get_text("timer_set_title"), f"{get_text('timer_set_msg')} {m} " + ("минут" if current_language == "ru" else "minutes"))


def cancel_shutdown():
	global countdown, countdown_job
	countdown = False
	if countdown_job:
		try:
			root.after_cancel(countdown_job)
		except Exception:
			pass
		countdown_job = None
	os.system("shutdown /a")
	for w in (toggle_btn, apply_btn, b_start):
		w.config(state="normal")
	status_label.config(text=get_text("status_cancelled"), fg=TEXT_DIM)
	countdown_label.config(text="")
	messagebox.showinfo(get_text("operation_title"), get_text("operation_cancelled"))


def make_btn(txt: str, cmd):
	b = tk.Button(
		buttons,
		text=txt,
		command=cmd,
		bg=BTN_BG,
		fg=TEXT,
		font=MONO_NORMAL,
		activebackground=BTN_HOVER,
		activeforeground=TEXT_BRIGHT,
		bd=2,
		relief="solid",
		width=14,
	)
	b.bind("<Enter>", lambda e: b.config(bg=BTN_HOVER, fg=TEXT_BRIGHT) if b["state"] == "normal" else None)
	b.bind("<Leave>", lambda e: b.config(bg=BTN_BG, fg=TEXT) if b["state"] == "normal" else None)
	return b


b_start = make_btn(get_text("btn_start"), start_shutdown)
b_start.pack(side="left", expand=True, padx=8)
make_btn(get_text("btn_stop"), cancel_shutdown).pack(side="right", expand=True, padx=8)


def rebuild_texts():
	header.config(text=get_text("header"))
	subtitle.config(text=get_text("subtitle"))
	footer.config(text=get_text("footer"))
	toggle_btn.config(text=get_text("btn_hide_manual") if show_manual.get() else get_text("btn_show_manual"))
	apply_btn.config(text=get_text("btn_apply_start"))
	lang_btn.config(text=get_text("language_btn"))
	if not countdown:
		status_label.config(text=get_text("status_ready"))
	display.config(text=format_time(val.get()))


root.mainloop()