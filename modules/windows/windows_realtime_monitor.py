import win32evtlog
import time
import csv
import os
from datetime import datetime

# Ensure 'reports/' directory exists
os.makedirs("reports", exist_ok=True)

LOG_TYPES = {
    "Security": "reports/windows_security.csv",
    "System": "reports/windows_system.csv",
    "Application": "reports/windows_application.csv"
}

def format_event(event):
    message = " | ".join(event.StringInserts) if hasattr(event, "StringInserts") and event.StringInserts else ""
    message = message.replace('\n', ' ').replace('\r', ' ')
    if len(message) > 300:
        message = message[:300] + "..."

    return {
        "TimeGenerated": event.TimeGenerated.Format("%Y-%m-%d %H:%M:%S"),
        "EventID": event.EventID,
        "Source": event.SourceName,
        "Category": event.EventCategory,
        "Type": event.EventType,
        "Message": message
    }

def write_event_to_csv(filename, event):
    write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "TimeGenerated", "EventID", "Source", "Category", "Type", "Message"
        ])
        if write_header:
            writer.writeheader()
        writer.writerow(format_event(event))

def monitor_log(log_type):
    print(f"[+] Real-time monitoring started for {log_type} log")
    server = 'localhost'
    log_handle = win32evtlog.OpenEventLog(server, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    last_record = win32evtlog.GetNumberOfEventLogRecords(log_handle)

    while True:
        total_records = win32evtlog.GetNumberOfEventLogRecords(log_handle)
        if total_records > last_record:
            events = win32evtlog.ReadEventLog(log_handle, flags, 0)
            new_events = events[:total_records - last_record]
            for event in new_events:
                write_event_to_csv(LOG_TYPES[log_type], event)
            last_record = total_records
        time.sleep(5)  # Poll every 5 seconds

def main():
    import threading
    for log in LOG_TYPES.keys():
        thread = threading.Thread(target=monitor_log, args=(log,), daemon=True)
        thread.start()

    print("[+] Real-time log monitoring running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Monitoring stopped.")

if __name__ == "__main__":
    main()
