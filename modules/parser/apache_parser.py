import re

def parse_apache_logs(file_path):
    logs = []
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<datetime>.*?)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" (?P<status>\d{3}) (?P<size>\d+)'
    )

    try:
        with open(file_path, 'r') as f:
            for line in f:
                match = log_pattern.search(line)
                if match:
                    log = {
                        'ip': match.group('ip'),
                        'datetime': match.group('datetime'),
                        'method': match.group('method'),
                        'url': match.group('url'),
                        'protocol': match.group('protocol'),
                        'status': int(match.group('status')),
                        'size': int(match.group('size')),
                    }
                    logs.append(log)
    except FileNotFoundError:
        print(f"[!] Apache log file not found: {file_path}")
    return logs
