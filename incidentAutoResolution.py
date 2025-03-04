#!/usr/bin/env python3

"""
-------------------Incident Detection & Auto-Resolution (Python & Azure Monitor)-------------------

Requires Python 3.13.2

This script automates active incident detection from azure monitor and auto resolve any service crash
    - Fetches active incident alerts from Azure Monitor
    - If an alert is related to a service crash, automatically attempts a restart.
    - Logs all resolutions and sends an email summary.

Developer Test Data:
mock api response = mock_azure_incidents.json
summary report = incident_resolution.log

-------------------DeveloperTested with mock data-------------------
"""

import requests
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# CONFIGURATION
AZURE_MONITOR_ALERTS_ENDPOINT = "https://management.azure.com/subscriptions/<SUBSCRIPTION_ID>/providers/Microsoft.AlertsManagement/alerts?api-version=2019-05-05"
ACCESS_TOKEN = "<YOUR_AZURE_BEARER_TOKEN>"
LOG_FILE = "incident_resolution.log"

EMAIL_FROM = "basnayakemsl@gmail.com"
EMAIL_TO = "basnayake92@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "basnayakemsl@gmail.com"
SMTP_PASSWORD = ""

# FETCH ACTIVE INCIDENTS
def fetch_active_incidents():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        # Actual API call for get incidents
        # response = requests.get(AZURE_MONITOR_ALERTS_ENDPOINT, headers=headers)
        # response.raise_for_status()
        # alerts = response.json()

        # Mock Data For Developer Testing
        with open("mock_azure_incidents.json") as f:
            alerts = json.load(f)
        return alerts.get("value", [])
    except Exception as e:
        print(f"[ERROR] Failed to fetch incidents: {e}")
        return []

# MOCK SERVICE RESTART
def restart_service(service_name):
    # Replace this with actual restart logic
    print(f"[INFO] Restarting service: {service_name}")
    return f"Service '{service_name}' restarted at {datetime.utcnow()}"

# LOG RESOLUTIONS
def log_resolution(alert_name, action):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.utcnow()} | Alert: {alert_name} | Action: {action}\n")

# SEND EMAIL SUMMARY
def send_email(summary):
    msg = MIMEText(summary)
    msg["Subject"] = "Incident Auto-Resolution Report"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print("[INFO] Email summary sent.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

# MAIN EXECUTION
def main():
    incidents = fetch_active_incidents()
    if not incidents:
        print("[INFO] No active incidents found.")
        return

    email_summary = "Incident Auto-Resolution Report\n\n"

    for alert in incidents:
        alert_name = alert.get("name")
        SERVICE_NAME = alert['properties']['essentials']['service']
        alert_description = alert.get("properties", {}).get("essentials", {}).get("description", "")

        print(f"[INFO] Processing alert: {alert_name}")

        if "crash" in alert_description.lower():
            action = restart_service(SERVICE_NAME)
            log_resolution(alert_name, action)
            email_summary += f"✔ Alert: {alert_name}\n   ➤ Action: {action}\n\n"
        else:
            email_summary += f"✖ Alert: {alert_name}\n   ➤ No action taken.\n\n"

    send_email(email_summary)


if __name__ == "__main__":
    main()
