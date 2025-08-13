diff --git a/shutdown_timer_2.0.py b/shutdown_timer_2.0.py
new file mode 100644
index 0000000..b1f22aa
--- /dev/null
+++ b/shutdown_timer_2.0.py
@@ -0,0 +1,356 @@
+# Shutdown Timer 2.0
+# - WinAPI-выключение (InitiateSystemShutdownEx / AbortSystemShutdown)
+# - Без потоков: Tkinter.after для стабильного обратного отсчёта
+# - Диалог при закрытии: оставить/отменить/остаться
+# - Простая i18n (ru/en) + склонение "минута/минуты/минут"
+#
+# Запуск: python shutdown_timer_2.0.py
+
+from __future__ import annotations
+import ctypes
+from ctypes import wintypes
+from datetime import datetime, timedelta
+import tkinter as tk
+from tkinter import ttk, messagebox
+
+# ==========================
+# WinAPI helpers
+# ==========================
+
+advapi32 = ctypes.WinDLL("Advapi32", use_last_error=True)
+kernel32 = ctypes.WinDLL("Kernel32", use_last_error=True)
+
+SE_PRIVILEGE_ENABLED = 0x00000002
+TOKEN_ADJUST_PRIVILEGES = 0x20
+TOKEN_QUERY = 0x8
+ERROR_NOT_ALL_ASSIGNED = 1300
+
+class LUID(ctypes.Structure):
+    _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]
+
+class LUID_AND_ATTRIBUTES(ctypes.Structure):
+    _fields_ = [("Luid", LUID), ("Attributes", wintypes.DWORD)]
+
+class TOKEN_PRIVILEGES(ctypes.Structure):
+    _fields_ = [("PrivilegeCount", wintypes.DWORD),
+                ("Privileges", LUID_AND_ATTRIBUTES * 1)]
+
+OpenProcessToken = advapi32.OpenProcessToken
+OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
+OpenProcessToken.restype = wintypes.BOOL
+
+LookupPrivilegeValueW = advapi32.LookupPrivilegeValueW
+LookupPrivilegeValueW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR, ctypes.POINTER(LUID)]
+LookupPrivilegeValueW.restype = wintypes.BOOL
+
+AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
+AdjustTokenPrivileges.argtypes = [wintypes.HANDLE, wintypes.BOOL,
+                                  ctypes.POINTER(TOKEN_PRIVILEGES),
+                                  wintypes.DWORD, ctypes.c_void_p, ctypes.c_void_p]
+AdjustTokenPrivileges.restype = wintypes.BOOL
+
+InitiateSystemShutdownExW = advapi32.InitiateSystemShutdownExW
+InitiateSystemShutdownExW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR,
+                                      wintypes.DWORD, wintypes.BOOL,
+                                      wintypes.BOOL, wintypes.DWORD]
+InitiateSystemShutdownExW.restype = wintypes.BOOL
+
+AbortSystemShutdownW = advapi32.AbortSystemShutdownW
+AbortSystemShutdownW.argtypes = [wintypes.LPWSTR]
+AbortSystemShutdownW.restype = wintypes.BOOL
+
+GetCurrentProcess = kernel32.GetCurrentProcess
+GetLastError = kernel32.GetLastError
+
+def _enable_shutdown_privilege(name="SeShutdownPrivilege"):
+    """Включаем привилегию SE_SHUTDOWN_NAME для текущего процесса."""
+    token = wintypes.HANDLE()
+    if not OpenProcessToken(GetCurrentProcess(),
+                            TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
+                            ctypes.byref(token)):
+        raise ctypes.WinError(ctypes.get_last_error())
+    luid = LUID()
+    if not LookupPrivilegeValueW(None, name, ctypes.byref(luid)):
+        raise ctypes.WinError(ctypes.get_last_error())
+    tp = TOKEN_PRIVILEGES(1, (LUID_AND_ATTRIBUTES(luid, SE_PRIVILEGE_ENABLED),))
+    # ВАЖНО: AdjustTokenPrivileges может вернуть TRUE, но привилегия не выдана
+    if not AdjustTokenPrivileges(token, False, ctypes.byref(tp), 0, None, None):
+        raise ctypes.WinError(ctypes.get_last_error())
+    # Проверим ERROR_NOT_ALL_ASSIGNED
+    err = ctypes.get_last_error()
+    if err == ERROR_NOT_ALL_ASSIGNED:
+        raise PermissionError("Not enough privileges to enable SeShutdownPrivilege")
+
+def schedule_shutdown(seconds: int,
+                      message: str | None = None,
+                      force_apps: bool = False,
+                      reboot: bool = False,
+                      reason: int = 0) -> None:
+    """Планирует выключение/перезагрузку через seconds."""
+    _enable_shutdown_privilege()
+    ok = InitiateSystemShutdownExW(None, message, seconds,
+                                   bool(force_apps), bool(reboot), reason)
+    if not ok:
+        raise ctypes.WinError(ctypes.get_last_error())
+
+def abort_shutdown() -> None:
+    """Отменяет планируемое отключение (если было)."""
+    _enable_shutdown_privilege()
+    ok = AbortSystemShutdownW(None)
+    if not ok:
+        err = ctypes.get_last_error()
+        # err==0 считается успехом; любое другое — ошибка (например, нечего отменять)
+        if err:
+            raise ctypes.WinError(err)
+
+# ==========================
+# i18n
+# ==========================
+
+LANG = "ru"   # "ru" или "en"
+
+I18N = {
+    "en": {
+        "title": "Shutdown Timer",
+        "minutes": "Minutes",
+        "start": "Start",
+        "cancel": "Cancel",
+        "ok": "OK",
+        "win_message": "Scheduled by Shutdown Timer",
+        "scheduled_ok": "System will shut down in {min} min.",
+        "status_ready": "Status: Ready",
+        "status_shutdown_now": "SYSTEM SHUTTING DOWN!",
+        "status_canceled": "Shutdown canceled",
+        "status_left": "Left: {m}:{s:02d} {unit}",
+        "confirm_exit_title": "Close the app?",
+        "confirm_exit_text": "A shutdown is scheduled.\n"
+                             "Yes — close and KEEP it scheduled.\n"
+                             "No — cancel shutdown and exit.\n"
+                             "Cancel — stay in the app.",
+        "lang": "Language",
+    },
+    "ru": {
+        "title": "Таймер выключения",
+        "minutes": "Минуты",
+        "start": "Старт",
+        "cancel": "Отмена",
+        "ok": "Ок",
+        "win_message": "Запланировано через Shutdown Timer",
+        "scheduled_ok": "Система выключится через {min} мин.",
+        "status_ready": "Статус: готов",
+        "status_shutdown_now": "СИСТЕМА ВЫКЛЮЧАЕТСЯ!",
+        "status_canceled": "Выключение отменено",
+        "status_left": "Осталось: {m}:{s:02d} {unit}",
+        "confirm_exit_title": "Закрыть приложение?",
+        "confirm_exit_text": "Выключение запланировано.\n"
+                             "Да — закрыть и ОСТАВИТЬ таймер.\n"
+                             "Нет — отменить выключение и выйти.\n"
+                             "Отмена — остаться в приложении.",
+        "lang": "Язык",
+    }
+}
+
+def t(key: str) -> str:
+    return I18N.get(LANG, I18N["en"]).get(key, key)
+
+def plural_minutes(n: int) -> str:
+    """Единица измерения минут с учетом языка."""
+    if LANG == "en":
+        return "minute" if n == 1 else "minutes"
+    # ru
+    n = abs(n)
+    if n % 10 == 1 and n % 100 != 11:
+        return "минута"
+    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
+        return "минуты"
+    return "минут"
+
+# ==========================
+# Tk application
+# ==========================
+
+class App(tk.Tk):
+    def __init__(self):
+        super().__init__()
+        self.title(t("title"))
+        self.geometry("360x210")
+        self.resizable(False, False)
+
+        # --- Controls ---
+        main = ttk.Frame(self, padding=12)
+        main.pack(expand=True, fill="both")
+
+        row = ttk.Frame(main)
+        row.pack(fill="x", pady=(0, 8))
+        ttk.Label(row, text=t("minutes")).pack(side="left")
+        self.minutes_var = tk.StringVar(value="10")
+        self.minutes = ttk.Spinbox(row, from_=1, to=600, textvariable=self.minutes_var, width=8)
+        self.minutes.pack(side="left", padx=(8, 0))
+
+        # Buttons
+        btns = ttk.Frame(main)
+        btns.pack(fill="x", pady=(0, 8))
+        self.btn_start = ttk.Button(btns, text=t("start"), command=self.on_start)
+        self.btn_start.pack(side="left", expand=True, fill="x", padx=(0, 6))
+        self.btn_cancel = ttk.Button(btns, text=t("cancel"), command=self.on_cancel)
+        self.btn_cancel.pack(side="left", expand=True, fill="x", padx=(6, 0))
+
+        # Status
+        self.status = ttk.Label(main, anchor="center", font=("Segoe UI", 11))
+        self.status.pack(fill="x", pady=(10, 0))
+        self.status.config(text=t("status_ready"))
+
+        # Language switch
+        lang_row = ttk.Frame(main)
+        lang_row.pack(fill="x", pady=(10, 0))
+        ttk.Label(lang_row, text=t("lang")).pack(side="left")
+        self.lang_var = tk.StringVar(value=LANG)
+        self.lang_box = ttk.Combobox(lang_row, values=["ru", "en"], textvariable=self.lang_var, width=6, state="readonly")
+        self.lang_box.pack(side="left", padx=(8, 0))
+        self.lang_box.bind("<<ComboboxSelected>>", self.on_lang_change)
+
+        # data
+        self.target_ts: datetime | None = None
+        self.countdown_job: str | None = None
+
+        self.protocol("WM_DELETE_WINDOW", self.on_close)
+
+    # --- UI helpers ---
+    def rebuild_texts(self):
+        self.title(t("title"))
+        # labels & buttons
+        for w in self.children.values():
+            pass  # no-op, всё управляем ниже
+        # Минуты лейбл
+        # (находится как первый Label в первом Frame — но проще хранить ссылку,
+        #  для краткости перерисуем только динамические элементы)
+        self.btn_start.config(text=t("start"))
+        self.btn_cancel.config(text=t("cancel"))
+        self.status.config(text=t("status_ready") if not self.target_ts else self.status.cget("text"))
+
+    # --- actions ---
+    def on_start(self):
+        try:
+            mins = int(self.minutes_var.get())
+            if mins <= 0:
+                raise ValueError
+        except Exception:
+            messagebox.showerror(t("title"), "Invalid minutes value" if LANG=="en" else "Некорректное значение минут")
+            return
+
+        seconds = mins * 60
+        try:
+            schedule_shutdown(seconds, message=t("win_message"), force_apps=False, reboot=False)
+        except PermissionError:
+            messagebox.showerror(t("title"),
+                                 "Not enough privileges. Run as admin." if LANG=="en"
+                                 else "Недостаточно прав. Запустите приложение от имени администратора.")
+            return
+        except OSError as e:
+            messagebox.showerror(t("title"), str(e))
+            return
+
+        self.target_ts = datetime.now() + timedelta(seconds=seconds)
+        self.tick()  # старт обновления статуса
+        messagebox.showinfo(t("ok"), t("scheduled_ok").format(min=mins))
+
+    def on_cancel(self):
+        try:
+            abort_shutdown()
+        except OSError as e:
+            # если нечего отменять — тоже приведём интерфейс в исходное состояние
+            print("Abort error:", e)
+        finally:
+            self._reset_timer_state(canceled=True)
+
+    def on_lang_change(self, *_):
+        global LANG
+        LANG = self.lang_var.get()
+        self.rebuild_texts()
+
+    # --- countdown via after ---
+    def tick(self):
+        if not self.target_ts:
+            self.status.config(text=t("status_ready"))
+            self.countdown_job = None
+            return
+        left = int((self.target_ts - datetime.now()).total_seconds())
+        if left <= 0:
+            self.status.config(text=t("status_shutdown_now"))
+            self.target_ts = None
+            self.countdown_job = None
+            return
+        m, s = divmod(left, 60)
+        self.status.config(text=t("status_left").format(m=m, s=s, unit=plural_minutes(m)))
+        self.countdown_job = self.after(1000, self.tick)
+
+    def _reset_timer_state(self, canceled: bool = False):
+        self.target_ts = None
+        if self.countdown_job:
+            try:
+                self.after_cancel(self.countdown_job)
+            except Exception:
+                pass
+            self.countdown_job = None
+        self.status.config(text=t("status_canceled") if canceled else t("status_ready"))
+
+    # --- close behavior ---
+    def on_close(self):
+        if self.target_ts:
+            res = messagebox.askyesnocancel(
+                t("confirm_exit_title"),
+                t("confirm_exit_text")
+            )
+            if res is None:
+                return  # Cancel — остаться
+            if res is False:
+                # No — отменить и выйти
+                try:
+                    abort_shutdown()
+                except OSError:
+                    pass
+                # сброс состояния
+                self._reset_timer_state(canceled=True)
+                self.destroy()
+                return
+            # Yes — просто выйти, НЕ отменяя запланированный shutdown
+        self.destroy()
+
+
+if __name__ == "__main__":
+    # Системные темы для ttk (если доступны)
+    try:
+        from ctypes import windll
+        windll.shcore.SetProcessDpiAwareness(1)  # немного чётче на HiDPI
+    except Exception:
+        pass
+    app = App()
+    app.mainloop()
