import os
import sys

# Add module path to import correctly
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules', 'windows'))

from windows_log_monitor import main as static_log_monitor
from windows_realtime_monitor import main as realtime_log_monitor

def main():
    print("\n==== Windows Log Analyzer ====\n")
    print("1. Static Log Collection (one-time snapshot)")
    print("2. Real-time Log Monitoring (continuous)")
    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "1":
        print("\n[+] Running static log collection...\n")
        static_log_monitor()
    elif choice == "2":
        print("\n[+] Running real-time log monitoring...\n")
        realtime_log_monitor()
    else:
        print("[!] Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
