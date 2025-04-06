import re

def parse_auth_log(filepath):
    parsed_logs = []
    
    pattern = re.compile(
    r'(?P<date>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+.*sshd.*(?P<status>Failed|Accepted)\s+password for (?:invalid user\s+)?(?P<user>\w+)\s+from\s+(?P<ip>\d+\.\d+\.\d+\.\d+)'
    )

    with open(filepath, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                parsed_logs.append({
                    'date': match.group('date'),
                    'status': match.group('status'),
                    'ip': match.group('ip'),
                    'user': match.group('user')
                })

    return parsed_logs