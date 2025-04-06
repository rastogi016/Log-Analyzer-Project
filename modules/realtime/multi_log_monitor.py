from datetime import datetime
import threading
import time
import re

def tail_log(file_path, callback):
    print(f"[🔍] Watching: {file_path}")
    try:
        with open(file_path, 'r') as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                callback(line.strip())
    except FileNotFoundError:
        print(f"[❌] File not found: {file_path}")

# Apache Log Handler
def handle_apache(line):
    match = re.search(r'"(\S+) (\S+) (\S+)" (\d{3})', line)
    if match:
        method, url, protocol, status = match.groups()
        status = int(status)
        if status >= 400:
            print(f"[🚨 Apache] {method} {url} returned {status}")
            log_alert(f"🚨 Apache - {method} {url} returned {status}")
        elif url.lower().startswith("/admin"):
            print(f"[⚠️ Apache] Admin page accessed: {method} {url}")
            log_alert(f"[⚠️ Apache] Admin page accessed: {method} {url}")

# Auth Log Handler
def handle_auth(line):
    if "Failed password" in line:
        print(f"[🚨 Auth] {line}")
        log_alert(f"[🚨 Auth] {line}")

    elif "Accepted password" in line:
        print(f"[✅ Auth] {line}")
        log_alert(f"[✅ Auth] {line}")

    elif "sudo" in line.lower():
        print(f"[⚠️ Sudo] {line}")
        log_alert(f"[⚠️ Sudo] {line}")

# Syslog Handler
def handle_syslog(line):
    if "error" in line.lower() or "fail" in line.lower():
        print(f"[⚠️ Syslog] {line}")
        log_alert(f"[⚠️ Syslog] {line}")

    elif "Started" in line or "Stopped" in line:
        print(f"[ℹ️ Syslog] {line}")
        log_alert(f"[ℹ️ Syslog] {line}")

def start_monitoring():
    paths_and_handlers = [
        ("logs/apache_sample.log", handle_apache),
        ("logs/auth_sample.log", handle_auth),
        ("logs/syslog_sample.log", handle_syslog)
    ]

    threads = []
    for path, handler in paths_and_handlers:
        t = threading.Thread(target=tail_log, args=(path, handler), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[🔚] Stopped monitoring.")

def log_alert(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('reports/alerts.log', 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {msg}\n")
