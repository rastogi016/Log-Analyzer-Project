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

    pattern = r'(\S+) (\S+) (\S+) \[([^\]]+)\] "(\S+) ([^"]+) HTTP/\d\.\d" (\d{3}) (\S+)'
    match = re.match(pattern, line)
    
    if match:
        ip = match.group(1)
        method = match.group(5)
        url = match.group(6)
        status = match.group(7)

        xss_Pattern = r"""(?i)(
            <\s*script[^>]*>.*?<\s*/\s*script\s*>      |  # <script>...</script>
            %3Cscript%3E.*?%3C/script%3E               |  # URL-encoded <script>
            javascript:                                |  # Inline JS
            on\w+\s*=\s*["']?[^"'>]+["']?              |  # Event handlers like onerror=
            alert\s*\(                                 |  # alert(
            prompt\s*\(                                |  # prompt(
            confirm\s*\(                               |  # confirm(
            eval\s*\(                                  |  # eval(
            document\.                                 |  # document.write, document.cookie, etc.
            window\.                                   |  # window.location, etc.
            <\s*(iframe|svg|img|video|audio|object)    |  # HTML tags commonly abused
            data:text/html                             |  # data URI with HTML
            &#x?[\da-f]+;                              |  # HTML encoded entities
            %[0-9a-f]{2}                               |  # URL encoded chars
            base64,                                    |  # base64 inline data
            <\s*meta[^>]*                              |  # meta tags (can redirect)
            <\s*body[^>]*onload                        # <body onload=
        )"""

        sqli_pattern = r"""
        (?i)  # Case-insensitive

        (?:\bOR\b|\bAND\b)\s+[^=]+(?:=|LIKE)\s+['"]?\w+['"]?   # e.g. OR 1=1
        |
        (?:\bUNION\b\s+SELECT\b)                              # UNION SELECT
        |
        (?:\bSELECT\b\s+.*?\bFROM\b)                          # SELECT ... FROM
        |
        (?:\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b)         # DML/DDL
        |
        (?:SLEEP\s*\(|BENCHMARK\s*\()                         # Time-based
        |
        (?:LOAD_FILE\s*\(|OUTFILE\b)                          # File-based
        |
        (?:INFORMATION_SCHEMA|mysql|pg_catalog)               # Info schemas
        |
        (?:VERSION\s*\(|USER\s*\()                            # Info functions
        |
        (?:EXEC\b|EXECUTE\b|xp_cmdshell)                      # RCE
        |
        (?:--|\#|/\*.*?\*/|%23|%2D%2D)                          # SQL comment
        """

        # XSS Detection
        if re.search(xss_Pattern, url, re.VERBOSE): 
            log_alert(f"🧨 XSS attempt from {ip} on {url}")

        # SQL Injection
        elif re.search(sqli_pattern, url, re.VERBOSE | re.IGNORECASE):
            log_alert(f"💉 SQL Injection attempt from {ip} on {url}")

        # LFI
        elif re.search(r"(?:\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c|%252e%252e%252f|%c0%ae%c0%ae|%uff0e%uff0e|/etc/passwd|\\etc\\passwd|file=)", url, re.IGNORECASE):
            log_alert(f"📂 LFI attempt from {ip} on {url}")


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
