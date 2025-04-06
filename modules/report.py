import csv
import os 

def export_to_csv(logs, filename='report.csv'):
    if not logs:
        print("[!] No data to export.")
        return

    os.makedirs('reports', exist_ok=True)
    filepath = os.path.join('reports', filename)

    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = logs[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(logs)

    print(f"[✔] Report saved to {filepath}")
