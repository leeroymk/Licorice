import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")
smtp_login = os.getenv("SMTP_LOGIN")
smtp_pwd = os.getenv("SMTP_PWD")
smtp_recipient = os.getenv("SMTP_RECIPIENT")


def send_email(subject="", message=""):
    msg = MIMEMultipart()
    msg["From"] = smtp_login
    msg["To"] = smtp_recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_login, smtp_pwd)
        server.sendmail(smtp_login, smtp_recipient, msg.as_string())
