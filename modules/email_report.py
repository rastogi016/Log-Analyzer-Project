import smtplib
import os
from email.message import EmailMessage

def send_email_report(to_email, subject, body, file_path, from_email, app_password):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)

    # Attach the CSV report
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Send the email via Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
        print(f"[📤] Report emailed to {to_email}")
    except Exception as e:
        print(f"[❌] Failed to send email: {e}")


'''
To add in main
from modules.email_report import send_email_report

# Email Credentials (use App Password if 2FA enabled)
FROM_EMAIL = 'your_email@gmail.com'
TO_EMAIL = 'recipient@example.com'
APP_PASSWORD = 'your_app_password'  # Use app password from Google

# Send filtered logs report
send_email_report(
    to_email=TO_EMAIL,
    subject='Filtered Logs Report',
    body='Attached is the filtered log analysis report.',
    file_path='reports/filtered_logs.csv',
    from_email=FROM_EMAIL,
    app_password=APP_PASSWORD
)
'''