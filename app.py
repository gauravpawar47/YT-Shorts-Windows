import os
import threading
import json
import re
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import yt_dlp
import shutil
import sys

# Constants
APP_DATA_FOLDER = os.path.join(os.getenv("LOCALAPPDATA"), "ShortsDownloader")
os.makedirs(APP_DATA_FOLDER, exist_ok=True)
HISTORY_FILE = os.path.join(APP_DATA_FOLDER, "download_history.json")
DEFAULT_FOLDER = os.path.join(Path.home(), "Downloads", "ShortsDownloader")

# Utilities
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*\n\r\t]', "_", name)

def clear_history_file():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)
    except Exception as e:
        print(f"Failed to clear history file: {e}")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-100:], f, indent=2)

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        return ffmpeg_path if os.path.exists(ffmpeg_path) else shutil.which("ffmpeg")
    return shutil.which("ffmpeg")

# Main App
class YouTubeDownloaderApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("📥 YouTube Shorts Downloader")
        self.geometry("800x600")
        self.resizable(False, False)

        self.download_path = ctk.StringVar(value=DEFAULT_FOLDER)
        self.history = load_history()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        self.build_ui()

    def build_ui(self):
        self.configure(bg='#2f2f2f')
        ctk.CTkLabel(self, text="YouTube Shorts Downloader", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self, text="Enter YouTube Shorts URL:", font=ctk.CTkFont(size=14)).pack(pady=(0, 10))

        self.url_box = ctk.CTkEntry(self, width=600, placeholder_text="Paste YouTube Shorts URL here...")
        self.url_box.pack(pady=(0, 10))

        ctk.CTkButton(self, text="📁 Choose Folder", command=self.browse_folder, width=180, height=40).pack(pady=(10, 20))
        self.path_label = ctk.CTkLabel(self, text=self.download_path.get(), text_color="gray", wraplength=600)
        self.path_label.pack(pady=5)

        self.theme_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(pady=(5, 10))

        ctk.CTkButton(self, text="⬇ Start Download", command=self.start_download, width=180, height=40).pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=10)
        self.progress.pack_forget()

        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14, weight="normal"))
        self.status_label.pack()

        ctk.CTkLabel(self, text="Recent Downloads (This Session):", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        self.history_box = ctk.CTkTextbox(self, height=150, width=600, font=ctk.CTkFont(size=12), wrap="word", corner_radius=10)
        self.history_box.pack(pady=(0, 10))
        self.history_box.configure(state="disabled")

        # Clear History button
        ctk.CTkButton(self, text="🧹 Clear History", command=self.clear_history, width=180, height=40).pack(pady=(5, 10))

        self.display_history()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path.set(folder)
            self.path_label.configure(text=folder)

    def toggle_theme(self):
        ctk.set_appearance_mode("Dark" if self.theme_switch.get() else "Light")

    def start_download(self):
        url = self.url_box.get().strip()
        if not url.startswith("http"):
            self.status_label.configure(text="❌ Please enter a valid YouTube Shorts URL.", text_color="red")
            return

        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            self.status_label.configure(
                text="❌ FFmpeg not found. Please install or bundle it with the app.",
                text_color="red"
            )
            return

        os.makedirs(self.download_path.get(), exist_ok=True)
        self.progress.set(0)
        self.progress.pack()
        self.status_label.configure(text="Starting download...", text_color="blue")

        threading.Thread(target=self.download_video, args=(url, ffmpeg_path), daemon=True).start()

    def download_video(self, url, ffmpeg_path):
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': ffmpeg_path,
            }

            def hook(d):
                if d['status'] == 'finished':
                    final_path = d['filename']
                    clean_title = self.extract_title(final_path)
                    if clean_title not in self.history:
                        self.history.append(clean_title)
                        save_history(self.history)
                        self.display_history()

                    self.progress.set(1)
                    self.status_label.configure(text="✅ Download completed.", text_color="green")

            ydl_opts['progress_hooks'] = [hook]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            self.status_label.configure(text=f"❌ Download failed: {str(e)}", text_color="red")

    def extract_title(self, filepath):
        base = os.path.basename(filepath)
        name, _ = os.path.splitext(base)
        return re.sub(r'-f\d+$', '', name)

    def display_history(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        for title in reversed(self.history[-5:]):
            self.history_box.insert("end", f"📽️ {title}\n")
        self.history_box.configure(state="disabled")

    def clear_history(self):
        # Clear the history file
        clear_history_file()
        self.history = []
        self.display_history()

if __name__ == "__main__":
    os.makedirs(DEFAULT_FOLDER, exist_ok=True)
    app = YouTubeDownloaderApp()
    app.mainloop()
