from collections import defaultdict

def detect_brute_force(logs, threshold=2):
    failed_attempts = defaultdict(int)
    
    for entry in logs:
        if entry['status'] == 'Failed':
            failed_attempts[entry['ip']] += 1

    suspicious_ips = {ip: count for ip, count in failed_attempts.items() if count >= threshold}
    
    return suspicious_ips

