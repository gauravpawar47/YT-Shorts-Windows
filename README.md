# 🎬 YouTube Shorts Downloader – Windows Software 🐍

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green?style=flat-square&logo=windows95)
![License](https://img.shields.io/github/license/yourusername/yourrepo?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows&style=flat-square)

> 🎉 All-in-one YouTube Shorts Downloader built in Python — includes  GUI, APIs, and reusable libraries. Installer setup via **Inno Setup** for smooth Windows installation.

---
## 🎬 Demo & Screenshots

### ▶️ Demo Video


>  [watch the demo](https://drive.google.com/file/d/1X2AfGPQtI39QUN9iu4pnw7wDXcnZNxzw/view?usp=sharing)_

---

## 🖼️ Screenshots

#### 1️⃣ Copy Link
![Copy Link](./screenshots/1_copy.png)

#### 2️⃣ Paste in App
![Paste in App](./screenshots/2_paste.png)

#### 3️⃣ Select the Folder
![Select Folder](./screenshots/3_select_folder.png)

#### 4️⃣ Click on Download
![Click Download](./screenshots/4_cliKC.png)

#### 5️⃣ Video has Downloaded
![Video Downloaded](./screenshots/5_download.png)

---

## 🧩 Features

- 🖥️ **User-Friendly GUI** – Simple interface for non-technical users  
- 📚 **Modular Architecture** – Reusable utilities like `ffmpeg_utils`, `file_utils`, and more  
- 📜 **Download History** – Tracks previously downloaded videos  
- 🧱 **Installer Ready** – Packaged with `.exe` and installer via Inno Setup  

---

## 📁 Folder Structure

```

📁 app/
┣ 📄 downloader.py         ← CLI / API logic
┣ 📄 ffmpeg\_utils.py       ← FFmpeg wrapper
┣ 📄 file\_utils.py         ← File handling
┣ 📄 main.py               ← GUI launcher
┗ 📄 app.spec              ← PyInstaller config

📁 dist/app/
┣ 📄 YouTubeShortsDownloader.exe
┣ 📄 ffmpeg.exe
┗ 📄 download\_history.json

📁 setup/
┣ 📄 setup\_v1.iss          ← Inno Setup script
┗ 📄 YouTubeShortsDownloader\_Installer.exe

📄 README.md
📄 YouTubeShortsDownloader.spec

````

---
### Create Installer:

* Open `setup/setup_v1.iss` with **Inno Setup Compiler**
* Click `Build`

---

> 🔗 *Crafted with ❤️ using Python, PyInstaller, and Inno Setup*
