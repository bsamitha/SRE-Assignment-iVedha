#!/usr/bin/env python3

"""
-------------------Root Cause Analysis Automation (Python & Logstash)-------------------

Requires Python 3.13.2

This script automates the root cause analysis from last 24 hours logs from logstash.
    - Collects log data from Logstash for the past 24 hours. .
    - Analyzes logs for common error patterns (e.g., connection timeouts, 500 errors).
    - Generates an automated incident summary with suggested remediation .

Developer Test Data:
mock api response = mock_logstash_response.json
summary report = error_summary.json

Note: This can be automated through a cron job and send a email notification for a better monitoring

-------------------DeveloperTested with mock data-------------------
"""

import requests
import json
import datetime
from collections import Counter

# Configuration
LOGSTASH_ENDPOINT = "http://<LOGSTASH_HOST>:9600/_search"
TIME_RANGE_HOURS = 24
ERROR_PATTERNS = {
    "OutOfMemoryError": "Analyze heap usage and increase JVM memory settings.",
    "Java heap space": "Heap size might be too small; consider tuning.",
    "GC overhead limit exceeded": "Review garbage collection logs and optimize.",
    "JDBCConnectionException": "Check database availability and connection pool settings.",
    "500": "Investigate application errors and server logs."
}
SUMMARY_FILE = "error_summary.json"


# Fetch Logs from Logstash
def fetch_logs():
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=TIME_RANGE_HOURS)

    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": start_time.isoformat(),
                    "lte": end_time.isoformat()
                }
            }
        },
        "size": 10000
    }


    try:
        # Actual api call for logstash to get the raw log
        # response = requests.post(LOGSTASH_ENDPOINT, json=query)
        # response.raise_for_status()
        # logs = response.json()

        # Mock Data For Developer Testing
        with open("mock_logstash_response.json", "r") as file:
            logs = json.load(file)
        return [hit["_source"]["message"] for hit in logs["hits"]["hits"]]
    except Exception as e:
        print(f"[ERROR] Failed to fetch logs: {e}")
        return []


# Analyze Logs for Error Patterns
def analyze_logs(logs):
    error_counts = Counter()
    matched_logs = []

    for log in logs:
        for pattern in ERROR_PATTERNS.keys():
            if pattern in log:
                error_counts[pattern] += 1
                matched_logs.append({"pattern": pattern, "log": log})
                break

    return error_counts, matched_logs


# Generate Incident Summary
def generate_summary(error_counts, matched_logs):
    summary = {
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "error_summary": [],
        "total_errors_found": sum(error_counts.values())
    }

    for error, count in error_counts.items():
        summary["error_summary"].append({
            "error": error,
            "count": count,
            "remediation": ERROR_PATTERNS[error]
        })  # Include first 5 matched logs as examples

    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"[INFO] Incident summary generated: {SUMMARY_FILE}")


def main():
    print("[INFO] Fetching logs from Logstash...")
    logs = fetch_logs()

    if not logs:
        print("[INFO] No logs found for the past 24 hours.")
        return

    print(f"[INFO] Analyzing {len(logs)} logs...")
    error_counts, matched_logs = analyze_logs(logs)

    if error_counts:
        print(f"[INFO] Errors detected: {dict(error_counts)}")
        generate_summary(error_counts, matched_logs)
    else:
        print("[INFO] No common error patterns detected.")


if __name__ == "__main__":
    main()
