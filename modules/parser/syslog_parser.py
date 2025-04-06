def parse_syslog(file_path):
    logs = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                log = {
                    'date': ' '.join(parts[0:3]),
                    'hostname': parts[3],
                    'message': ' '.join(parts[4:])
                }
                logs.append(log)
    except FileNotFoundError:
        print(f"[!] Syslog file not found: {file_path}")
    return logs
