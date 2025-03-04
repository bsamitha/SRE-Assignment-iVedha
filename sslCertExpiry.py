#!/usr/bin/env python3

"""
-------------------SSL Certificate Expiry Monitor-------------------

Requires Python 3.13.2

This script automates alerting SSL certificate expiration.
    - Scan domain names from 'domains.txt'.
    - Check the SSL certificate expiration date of each domain.
    - Send an email alert if any certificate is expiring within the next 15 days.

Developer Test Data:
domain - google.com - Expires on 2025-05-21 15:32:54 (78 days left)

Email Settings:
    - SMTP Server   : smtp.gmail.com
    - Port          : 587 (TLS)

Notes:
    - Use an App Password instead of your regular Gmail password.
    - App Password can be generated from your Google Account's security settings.
    - Run as a Scheduled Task on Windows or as a Cron Job on Linux

-------------------DeveloperTested-------------------
"""


import socket
import ssl
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Email settings (modify with your details)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "basnayakemsl@gmail.com"
EMAIL_PASS = ""
EMAIL_TO = "basnayake92@gmail.com"


def send_alert(domain, expiry_date):
    subject = f"SSL Certificate Expiring Soon: {domain}"
    body = f"The SSL certificate for {domain} expires on {expiry_date}."
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = EMAIL_USER
    message["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(message)


def get_ssl_expiry(domain):
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            expiry_str = cert["notAfter"]
            return datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")


def main():
    with open("domains.txt", "r") as file:
        domains = [line.strip() for line in file if line.strip()]

    for domain in domains:
        try:
            expiry_date = get_ssl_expiry(domain)
            days_left = (expiry_date - datetime.utcnow()).days
            print(f"{domain} - Expires on {expiry_date} ({days_left} days left)")
            if days_left <= 150:
                print(domain)
                send_alert(domain, expiry_date)
        except Exception as e:
            print(f"Error checking {domain}: {e}")


if __name__ == "__main__":
    main()
