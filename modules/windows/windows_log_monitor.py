import win32evtlog
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
    if isinstance(event, dict):  # already formatted
        return event

    message = " | ".join(event.StringInserts) if hasattr(event, "StringInserts") and event.StringInserts else ""

    message = message.replace('\n', ' ').replace('\r', ' ')
    if len(message) > 300:
        message = message[:300] + "..."

    return {
        "TimeGenerated": event.TimeGenerated.Format("%Y-%m-%d %H:%M:%S") if hasattr(event, "TimeGenerated") else "",
        "EventID": getattr(event, "EventID", ""),
        "Source": getattr(event, "SourceName", ""),
        "Category": getattr(event, "EventCategory", ""),
        "Type": getattr(event, "EventType", ""),
        "Message": message
    }


def write_event_to_csv(filename, events):
    # Check if file exists and is empty (write header only once)
    write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "TimeGenerated", "EventID", "Source", "Category", "Type", "Message"
        ])

        if write_header:
            writer.writeheader()

        for event in events:
            formatted = format_event(event)
            writer.writerow(formatted)

def read_and_log(log_type, max_events=20):
    server = 'localhost'
    path = LOG_TYPES[log_type]

    try:
        handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

        events = win32evtlog.ReadEventLog(handle, flags, 0)
        print(f"[+] {log_type} log: {len(events)} records found")

        for event in events[:max_events]:
            event_data = format_event(event)
            write_event_to_csv(path, [event_data])

    except Exception as e:
        print(f"[!] Failed to read {log_type} log: {e}")

def main():
    for log in LOG_TYPES.keys():
        read_and_log(log)

def start_monitoring():
    main()

