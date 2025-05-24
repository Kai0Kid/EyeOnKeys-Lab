# EyeOnKeys-Lap : Educational project for capturing keyboard input on Windows. For ethical research and cybersecurity training purposes only.

# EyeOnKeys-Lab 🔍⌨️

**EyeOnKeys-Lab** is a Windows-based keystroke logging project developed strictly for educational and cybersecurity research purposes.

## 🚨 Disclaimer

> ⚠️ This project is intended **for ethical hacking, cybersecurity training, and educational use only**.  
> Do **not** use this tool on machines you do not own or without explicit permission.  
> The author is **not responsible** for any misuse or damage caused by this code.

---

## 🎯 Purpose

This project demonstrates how keystrokes can be captured at the system level using Windows APIs. It serves as a lab exercise for:

- Understanding low-level input interception techniques
- Learning how keyloggers work (so you can detect or defend against them)
- Experimenting with Windows hooks and message loops

---

⚙️ Features
🛑 Single instance enforcement
Prevents multiple instances from running simultaneously using a Windows mutex.

🖥️ System info collection
Retrieves username, hostname, local IP, and public IP for context in each log.

⌨️ Keystroke logging
Captures all keystrokes (including special keys) using the pynput library.

🧠 In-memory logging
Stores keystrokes in memory to minimize disk activity and evade detection.

📤 Periodic log upload
Automatically sends logs every 30 minutes via Discord webhook.

🔐 Base64 log encoding
Encodes log contents before uploading, helping to obfuscate sensitive data during transit.

📁 Temp file management
Uses secure temporary files for transferring logs, then deletes them after sending.

🪟 Windows auto-start
If compiled (e.g., with PyInstaller), the program will persist via Windows Registry on user login.

❌ Failsafe exit handling
Ensures any unsent logs are delivered when the application exits gracefully or abruptly.
---

## 📂 Log Structure (after decoding base64)

Once the file is decoded, it looks like this:

```
User: Kai0Kid
Hostname: DESKTOP-ABC
Local IP: 192.168.1.10
Public IP: 171...***
[ENTER]Hello world[SPACE]Bye[BACKSPACE]
```

## 📦 Requirements

- Python 3.6+
- Windows OS (Tested on Windows 7, Windows 10)
- Required packages: `pywin32`, `keyboard`, etc.

Install dependencies with:

```bash
pip install -r requirements.txt

💡 You can customize the project as you like, such as modifying it to send logs via Telegram, Discord, Gmail, or any other preferre.


GitHub: https://github.com/Kai0Kid
