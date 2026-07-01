# 🌐 Windows Multi-Monitor Language Notifier

A lightweight, high-performance Windows language switcher notifier built with Python and Tkinter. It displays a modern, semi-transparent overlay widget at the center of **all connected screens** whenever the system input language changes. 

Designed to be ultra-clean, completely unobtrusive, and highly optimized for daily productivity.

---

## ✨ Key Features

* **🖥️ Full Multi-Monitor Support:** Automatically detects all connected displays (independent of resolution or individual scaling) and shows the indicator perfectly centered on every screen simultaneously.
* **🖱️ Mouse Click-Through:** Embedded with Native Windows API styles (`WS_EX_TRANSPARENT`), allowing your mouse cursor to click straight through the widget. It will never hijack your focus or interrupt your typing rhythm.
* **🎬 60 FPS Smooth Fade-out:** Once the display duration is met (0.75s), the widget elegantly fades into thin air at 60 frames per second (16ms timestep) rather than vanishing abruptly.
* **⚡ Ultra Lightweight & Efficient:** Uses a polling cycle architecture optimized at ~80ms combined with Tkinter's event loop queue. It runs smoothly silently in the background consuming **~0% CPU usage** and virtually zero memory.
* **⌨️ Universal Hotkey Compatible:** Listens directly to the Windows Active Window Keyboard Layout. Whether you toggle your language via the Grave Accent (`~`), `Alt+Shift`, `Win+Space`, or a taskbar click, it captures the change perfectly.
* **🔮 Future-Proof Mapping:** Built upon a clean class structure utilizing `PRIMARYLANGID`. Adding or modifying supported languages in the future is as simple as inserting a hex key into the `self.lang_map` dictionary.

---

## 🛠️ Installation & Usage

### 1. Prerequisites
This application requires **Windows OS** and an installed instance of **Python**.

### 2. Install Dependencies
Open your Command Prompt / Terminal and install the required Windows API wrapper:
```bash
pip install pywin32
