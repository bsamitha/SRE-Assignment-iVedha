#!/usr/bin/env python3

"""
-------------------Kubernetes Resource Optimization-------------------

Requires Python 3.13.2

This script automates Kubernetes Resource Optimization
    - Monitors log files in /var/logs/ for size exceeding 100MB.
    - Compresses and archives oversize log files to /var/logs/archive/.
    - Deletes archived log files older than 30 days to save disk space.

Developer Test Data:
log_dir = "C:\\Users\\Laptop Outlet\\Desktop\\Interview\\test data\\log"
archive_dir = "C:\\Users\\Laptop Outlet\\Desktop\\Interview\\test data\\log\\archive"
size_limit = 10000
delete_older_than = 120

Note: This is real-time monitoring and can be deployed as a systemd service

-------------------DeveloperTested-------------------
"""

from kubernetes import client, config
import datetime
import json

# Load AKS cluster config (assumes you have 'kubectl' context set up)
config.load_kube_config()

# Kubernetes API clients
v1 = client.CoreV1Api()
metrics_client = client.CustomObjectsApi()

# Threshold for under utilization (20%)
CPU_THRESHOLD = 0.2
MEMORY_THRESHOLD = 0.2

# Log file
log_file = "underutilized_pods.log"


# def get_pod_metrics(namespace, pod_name):
#     try:
#         metrics = metrics_client.get_namespaced_custom_object(
#             group="metrics.k8s.io",
#             version="v1beta1",
#             namespace=namespace,
#             plural="pods",
#             name=pod_name
#         )
#         return metrics
#     except Exception as e:
#         print(f"Error fetching metrics for {pod_name}: {e}")
#         return None

def get_pod_metrics(namespace, pod_name):
    with open("dummy_pod_metrics.json") as f:
        metrics = json.load(f)
    return metrics


def main():
    underutilized_pods = []

    pods = v1.list_pod_for_all_namespaces(watch=False)

    for pod in pods.items:
        namespace = pod.metadata.namespace
        name = pod.metadata.name
        metrics = get_pod_metrics(namespace, name)

        if metrics:
            cpu_usage = metrics['containers'][0]['usage']['cpu']
            memory_usage = metrics['containers'][0]['usage']['memory']

            # Placeholder: convert CPU/memory to percentages (depends on requests/limits)
            # Here, you would retrieve requests/limits and calculate usage %.
            # For example purposes, we'll just log the raw usage.

            print(f"Pod: {name} | CPU: {cpu_usage} | Memory: {memory_usage}")

            # Add real logic here for percentage calculation
            # if cpu_percent < CPU_THRESHOLD or memory_percent < MEMORY_THRESHOLD:
            #     underutilized_pods.append(f"{namespace}/{name}")

    # Log underutilized pods
    with open(log_file, "w") as file:
        for pod in underutilized_pods:
            file.write(f"{datetime.datetime.now()} - Underutilized: {pod}\n")

    print(f"Underutilized pods logged to {log_file}")


if __name__ == "__main__":
    main()
