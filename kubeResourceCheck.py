from kubernetes import client, config
import logging
import json

# Setup logging
logging.basicConfig(
    filename="underutilized_pods.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_pod_metrics():
    # Load kubeconfig (assuming it's already configured for AKS)
    # config.load_kube_config()
    #
    # v1 = client.CoreV1Api()
    # custom_api = client.CustomObjectsApi()

    # Get all pods across all namespaces
    # pods = v1.list_pod_for_all_namespaces(watch=False)

    with open("dummy_pod_metrics.json", "r") as file:
        pods = json.load(file)

    underutilized_pods = []

    for pod in pods['pods']:
        namespace = pod['namespace']
        pod_name = pod['name']
        metrics = pod['metrics']
        try:
            # Get metrics from metrics.k8s.io API
            total_cpu_usage = 0
            total_memory_usage = 0

            for container in metrics['containers']:
                cpu = container['usage']['cpu']
                memory = container['usage']['memory']

                # Convert CPU and memory to millicores and Mi
                cpu_millicores = parse_cpu(cpu)
                memory_mi = parse_memory(memory)

                total_cpu_usage += cpu_millicores
                total_memory_usage += memory_mi

            # Example thresholds (adjust as per actual pod requests/limits)
            cpu_threshold = 200  # 20% of 1000m (1 core)
            memory_threshold = 100  # 20% of 500Mi

            if total_cpu_usage < cpu_threshold and total_memory_usage < memory_threshold:
                underutilized_pods.append((namespace, pod_name, total_cpu_usage, total_memory_usage))
                logging.info(f"Underutilized Pod: {namespace}/{pod_name} - CPU: {total_cpu_usage}m, Memory: {total_memory_usage}Mi")

        except client.exceptions.ApiException as e:
            logging.error(f"Failed to fetch metrics for pod {namespace}/{pod_name}: {e}")

    print(f"Found {len(underutilized_pods)} underutilized pods. Check 'underutilized_pods.log' for details.")

def parse_cpu(cpu_str):
    if cpu_str.endswith('n'):
        return int(cpu_str.rstrip('n')) / 1e6
    if cpu_str.endswith('u'):
        return int(cpu_str.rstrip('u')) / 1000
    if cpu_str.endswith('m'):
        return int(cpu_str.rstrip('m'))
    return int(cpu_str) * 1000

def parse_memory(mem_str):
    if mem_str.endswith('Ki'):
        return int(mem_str.rstrip('Ki')) / 1024
    if mem_str.endswith('Mi'):
        return int(mem_str.rstrip('Mi'))
    if mem_str.endswith('Gi'):
        return int(mem_str.rstrip('Gi')) * 1024
    return int(mem_str) / (1024 * 1024)

if __name__ == "__main__":
    get_pod_metrics()
