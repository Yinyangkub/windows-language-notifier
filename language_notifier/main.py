import ctypes
import tkinter as tk
from threading import Thread
import win32api
import win32gui
import win32process

# ดึงฟังก์ชันสำหรับตั้งค่าให้เมาส์คลิกทะลุได้ (Click-Through)
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020


class PerfectLanguageNotifier:

    def __init__(self):
        self.lang_map = {
            0x0409: "ENG",
            0x041E: "TH",
            0x0411: "JPN",
            0x040C: "FRA",
        }
        self.last_lang = self.get_current_keyboard_language()
        self.widgets = []
        self.main_root = None
        self.fade_job = None
        self.close_job = None

    def get_current_keyboard_language(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None
            thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
            layout_id = win32api.GetKeyboardLayout(thread_id)
            return self.lang_map.get(layout_id & 0xFFFF, None)
        except Exception:
            return None

    def make_click_through(self, hwnd):
        """ทำให้หน้าต่างโปร่งใสต่อเมาส์ สามารถคลิกทะลุผ่านไปข้างหลังได้ พิมพ์งานไม่สะดุด"""
        try:
            styles = win32gui.GetWindowLong(hwnd, GWL_EXSTYLE)
            win32gui.SetWindowLong(
                hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED | WS_EX_TRANSPARENT
            )
        except Exception:
            pass

    def show_notification(self, lang_text):
        """แสดงผล Widget ทุกจอ พร้อมระบบ Reset คิวเดิมหากกดรัวๆ"""
        # เคลียร์คิวเวลาเก่าทิ้งทันทีหากมีการกดรัวๆ
        if self.fade_job:
            self.main_root.after_cancel(self.fade_job)
        if self.close_job:
            self.main_root.after_cancel(self.close_job)

        self.close_widgets()
        monitors = win32api.EnumDisplayMonitors()

        for monitor in monitors:
            hMonitor, hdcMonitor, rect = monitor
            left, top, right, bottom = rect

            w_width, w_height = 160, 80
            x = left + ((right - left) // 2) - (w_width // 2)
            y = top + ((bottom - top) // 2) - (w_height // 2)

            root = tk.Toplevel(self.main_root) if self.main_root else tk.Tk()
            if not self.main_root:
                self.main_root = root

            root.overrideredirect(True)
            root.attributes("-topmost", True)
            root.attributes("-alpha", 0.65)  # เริ่มต้นที่ความจาง 65%
            root.configure(bg="#1E1E1E")  # สีเทาเข้มหรูๆ
            root.geometry(f"{w_width}x{w_height}+{x}+{y}")

            # สั่งขอบมนโฉบเฉี่ยวสไตล์ Modern UI (ทางเลือก)
            root.label = tk.Label(
                root,
                text=lang_text,
                font=("Segoe UI", 26, "bold"),
                fg="#FFFFFF",
                bg="#1E1E1E",
            )
            root.label.pack(expand=True)

            self.widgets.append(root)

            # อัปเดตเพื่อให้ได้ Windows HWND มาทำ Click-Through
            root.update()
            hwnd = win32gui.FindWindow(None, root.title())
            if hwnd:
                self.make_click_through(hwnd)

        # ตั้งเวลา: แสดงผลเต็มๆ 800ms จากนั้นเริ่มเฟดหายตอนท้ายจนครบ 1 วินาที (1000ms)
        self.fade_job = self.main_root.after(800, self.fade_out, 0.65)

    def fade_out(self, current_alpha):
        """ค่อยๆ ลดค่าความสว่างลงทีละนิดเพื่อให้ดูนุ่มนวลตอนหายไป"""
        if current_alpha > 0.0:
            new_alpha = current_alpha - 0.1
            for w in self.widgets:
                try:
                    w.attributes("-alpha", max(0.0, new_alpha))
                except Exception:
                    pass
            # ทำซ้ำทุกๆ 30 มิลลิวินาทีจนกว่าจะจางหายไปสนิท
            self.fade_job = self.main_root.after(
                30, self.fade_out, new_alpha
            )
        else:
            self.close_widgets()

    def close_widgets(self):
        for w in self.widgets:
            try:
                if w != self.main_root:
                    w.destroy()
                else:
                    w.withdraw()
            except Exception:
                pass
        self.widgets.clear()

    def monitor_language_loop(self):
        """ระบบดักจับภาษาที่ตอบสนองไวแต่ใช้กำลังเครื่องต่ำมาก"""
        while True:
            # ใช้ sleep 0.08s (80ms) ไวกว่าเดิม ทันใจวัยรุ่น พิมพ์เร็วแค่ไหนก็ดักทัน
            win32api.Sleep(80)
            current_lang = self.get_current_keyboard_language()

            if current_lang and current_lang != self.last_lang:
                self.last_lang = current_lang
                if self.main_root:
                    self.main_root.after_idle(
                        self.show_notification, current_lang
                    )


if __name__ == "__main__":
    notifier = PerfectLanguageNotifier()

    hidden_root = tk.Tk()
    hidden_root.withdraw()
    notifier.main_root = hidden_root

    monitor_thread = Thread(
        target=notifier.monitor_language_loop, daemon=True
    )
    monitor_thread.start()

    hidden_root.mainloop()