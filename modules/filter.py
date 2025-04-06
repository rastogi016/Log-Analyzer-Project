def filter_noise(logs, trusted_ips=None, ignored_users=None):
    trusted_ips = trusted_ips or []
    ignored_users = ignored_users or []

    filtered_logs = []

    for log in logs:
        ip = log.get('ip', '')
        user = log.get('user', '')  # We'll update parser to capture user too

        if ip in trusted_ips:
            continue
        if user in ignored_users:
            continue

        filtered_logs.append(log)

    return filtered_logs
