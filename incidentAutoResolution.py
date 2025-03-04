import smtplib
import logging
from email.mime.text import MIMEText
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from azure.monitor.query import LogsQueryStatus

# ======================
# Configuration Section
# ======================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "recipient_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

AZURE_LOG_WORKSPACE_ID = "<YOUR_LOG_WORKSPACE_ID>"
QUERY_TIME_RANGE = "PT1H"  # Last 1 hour

SERVICE_RESTART_COMMANDS = {
    "nginx": "sudo systemctl restart nginx",
    "apache2": "sudo systemctl restart apache2"
}

# ======================
# Logging Setup
# ======================

logging.basicConfig(
    filename="incident_resolution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ======================
# Fetch Azure Alerts
# ======================

def fetch_active_alerts():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    query = """
    AzureDiagnostics
    | where Category == "ServiceHealth"
    | where Status_s == "Active"
    | project TimeGenerated, Resource, AlertName_s, Description, Status_s
    """

    result = client.query_workspace(
        workspace_id=AZURE_LOG_WORKSPACE_ID,
        query=query,
        timespan=QUERY_TIME_RANGE
    )

    alerts = []
    if result.status == LogsQueryStatus.SUCCESS:
        for row in result.tables[0].rows:
            alerts.append({
                "time": row[0],
                "resource": row[1],
                "name": row[2],
                "description": row[3],
                "status": row[4]
            })
    else:
        logging.error("Failed to fetch Azure alerts.")

    return alerts


# ======================
# Restart Service (Mock)
# ======================

def restart_service(resource, service):
    restart_command = SERVICE_RESTART_COMMANDS.get(service)
    if restart_command:
        logging.info(f"Restarting {service} on {resource}.")
        # Actual SSH/remote execution code would go here.
        return True
    else:
        logging.error(f"No restart command defined for {service}.")
        return False


# ======================
# Send Email Summary
# ======================

def send_email_summary(resolved, failed):
    body = f"Resolved Incidents:\n"
    for item in resolved:
        body += f"- {item}\n"
    body += "\nFailed Resolutions:\n"
    for item in failed:
        body += f"- {item}\n"

    msg = MIMEText(body)
    msg["Subject"] = "[Incident Auto-Resolution Report]"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        logging.info("Summary email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


# ======================
# Main Process
# ======================

def main():
    alerts = fetch_active_alerts()
    resolved = []
    failed = []

    for alert in alerts:
        if "crash" in alert["description"].lower():
            service = "nginx"  # Simplified; map from resource if needed.
            success = restart_service(alert["resource"], service)
            if success:
                message = f"{service} on {alert['resource']} restarted."
                resolved.append(message)
            else:
                message = f"{service} on {alert['resource']} failed to restart."
                failed.append(message)

    send_email_summary(resolved, failed)


if __name__ == "__main__":
    main()
