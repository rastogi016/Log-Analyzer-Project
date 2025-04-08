# 🛡️ Real-Time Log Analysis & Alerting Tool

A Python-based log analysis tool that monitors system logs (Auth, Syslog, Apache) **and Windows event logs** in real-time or statically to detect suspicious activities such as brute-force attacks, unauthorized access, and system errors. Generates structured reports and saves alerts for auditing purposes.

---

## 🚀 Features

- 🔍 **Multi-log support**:
  - Linux: Auth logs, Syslogs, Apache access logs.
  - Windows: Security, System, and Application logs.
- 🕒 **Real-time & static log monitoring** (user can choose).
- 🧠 **Noise filtering** to ignore irrelevant entries.
- 🚨 **Suspicious activity detection**:
  - Brute-force login attempts
  - Unusual status codes in Apache logs
  - Access to sensitive resources (e.g., `/admin`)
- 📊 **Report generation** in CSV format.
- 📁 **Alert logging** to a file (`alerts.log`) for incident tracking.
- 🪟 **Windows Event Log support** using `pywin32`.
- ⚙️ Modular and extensible design.

---

## 📁 Folder Structure

log-analyzer/ ├── main.py ├── modules/ │ ├── parser/ │ │ ├── apache_parser.py │ │ ├── auth_parser.py │ │ └── syslog_parser.py │ ├── realtime/ │ │ └── multi_log_monitor.py │ └── windows/ │ ├── windows_log_monitor.py # Static log reader │ └── windows_realtime_monitor.py # Real-time event listener ├── reports/ │ ├── apache_report.csv │ ├── auth_report.csv │ ├── syslog_report.csv │ ├── windows_application.csv │ ├── windows_security.csv │ ├── windows_system.csv │ └── alerts.log └── sample_logs/ ├── apache.log ├── auth.log └── syslog.log

---

## ⚙️ How It Works

1. Parses multiple logs line-by-line using regex patterns (for Linux) or event handlers (for Windows).
2. Monitors logs in real-time using background threads (or reads static logs once).
3. Filters out noisy log entries.
4. Detects abnormal behavior and generates alerts.
5. Logs alerts and creates CSV reports.

---

## 🧪 Sample Logs (Linux Only)

Place sample log files in the `sample_logs/` directory:
- `auth.log`
- `syslog.log`
- `apache.log`

These files are used for initial parsing and testing.

---

## ✅ How to Run

```bash
# Clone the repo
git clone https://github.com/rastogi016/log-analyzer.git
cd log-analyzer
```

# Run main selector script
- python mainWin.py
- python mainLinux.py

# Requirements
- Python 3.8+
Runs on both Linux and Windows

### For Windows logs:
- Install pywin32 using pip install pywin32

# Use Cases
- System log monitoring
- Security audit preparation
- Brute-force detection
- SQL Injection Detection
- XSS Detection
- LFI Detection
- Windows Event Log Auditing

# Author
Yash Rastogi
GitHub: rastogi016
