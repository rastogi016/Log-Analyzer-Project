# 🛡️ Real-Time Log Analysis & Alerting Tool

A Python-based log analysis tool that monitors system logs (Auth, Syslog, Apache) in real-time to detect suspicious activities such as brute-force attacks, unauthorized access, and system errors. Generates structured reports and saves alerts for auditing purposes.

---

## 🚀 Features

- 🔍 **Multi-log support**: Auth logs, Syslogs, and Apache access logs.
- 🕒 **Real-time monitoring** using multi-threading.
- 🧠 **Noise filtering** to ignore irrelevant entries.
- 🚨 **Suspicious activity detection**:
  - Brute-force login attempts
  - Unusual status codes in Apache logs
  - Access to sensitive resources (e.g., `/admin`)
- 📊 **Report generation** in CSV format.
- 📁 **Alert logging** to a file (`alerts.log`) for incident tracking.
- ⚙️ Modular and extensible design.

---

## 📁 Folder Structure

log-analyzer/ ├── main.py ├── modules/ │ ├── parser/ │ │ ├── apache_parser.py │ │ ├── auth_parser.py │ │ └── syslog_parser.py │ └── realtime/ │ └── multi_log_monitor.py ├── reports/ │ ├── apache_report.csv │ ├── auth_report.csv │ ├── syslog_report.csv │ └── alerts.log └── sample_logs/ ├── apache.log ├── auth.log └── syslog.log


---

## ⚙️ How It Works

1. Parses multiple logs line-by-line using regex patterns.
2. Monitors logs in real-time using background threads.
3. Filters out noisy log entries.
4. Detects abnormal behavior and generates alerts.
5. Logs alerts and creates CSV reports.

---

## 🧪 Sample Logs

You can place sample log files in the `sample_logs/` directory:
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

# Run the analyzer
python main.py
```
---

# 🔧 Requirements
Python 3.8+
Runs on both Linux and Windows
No external libraries required (built with standard Python modules)

## Use Cases
System log monitoring
Security audit preparation
Brute-force detection
