from modules.parser.auth_parser import parse_auth_log
from modules.parser.syslog_parser import parse_syslog
from modules.parser.apache_parser import parse_apache_logs

from modules.realtime.multi_log_monitor import start_monitoring

from modules.filter import filter_noise
from modules.alert import detect_brute_force
from modules.report import export_to_csv

def main():
    # Authlog Handler
    authlogs = parse_auth_log('logs/Linux/auth_sample.log')
    filtered_logs = filter_noise(authlogs, trusted_ips=['192.168.1.20'], ignored_users=['testuser'])

    print("[+] Filtered Logs:")
    for log in filtered_logs:
        print(log)

    export_to_csv(filtered_logs, filename='filtered_logs.csv')

    alerts = detect_brute_force(filtered_logs)

    if alerts:
        alert_data = [{'ip': ip, 'count': count} for ip, count in alerts.items()]
        export_to_csv(alert_data, filename='alerts.csv')
    else:
        print("[✔] No brute-force alerts generated.")
    
    # Syslog Handler
    syslogs = parse_syslog('logs/Linux/syslog_sample.log')
    export_to_csv(syslogs, filename='syslogs.csv')

    # Apache Log Handler
    apache_logs = parse_apache_logs('logs/apache_sample.log')
    export_to_csv(apache_logs, filename='apache_logs.csv')

    # For Realtime Monitoring 
    start_monitoring()

if __name__ == "__main__":
    main()
