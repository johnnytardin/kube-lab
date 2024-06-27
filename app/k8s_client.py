import yaml

from kubernetes import client, config
from app.config import Config


def load_kube_config():
    if Config.CLUSTER_URL:
        with open(Config.KUBECONFIG, "r") as f:
            kubeconfig = yaml.safe_load(f)

        kubeconfig["clusters"][0]["cluster"]["server"] = Config.CLUSTER_URL
        config.load_kube_config_from_dict(config_dict=kubeconfig)
    else:
        config.load_kube_config(config_file=Config.KUBECONFIG)


def get_nodes():
    load_kube_config()
    v1 = client.CoreV1Api(None)
    nodes = v1.list_node().items
    return [node.metadata.name for node in nodes]


def get_namespaces():
    load_kube_config()
    v1 = client.CoreV1Api(None)
    namespaces = v1.list_namespace().items
    return [ns.metadata.name for ns in namespaces]


def create_namespace(name):
    load_kube_config()
    v1 = client.CoreV1Api(None)
    body = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
    v1.create_namespace(body=body)

def get_pods(namespace):
    load_kube_config()
    v1 = client.CoreV1Api()
    if namespace:
        pods = v1.list_namespaced_pod(namespace)
    else:
        pods = v1.list_pod_for_all_namespaces()
    return [pod.metadata.name for pod in pods.items]

def get_cluster_info():
    load_kube_config()
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    batch_v1 = client.BatchV1Api()
    networking_v1 = client.NetworkingV1Api()

    try:
        cluster_info = {
            "nodes": len(v1.list_node().items),
            "namespaces": len(v1.list_namespace().items),
            "pods": len(v1.list_pod_for_all_namespaces().items),
            "deployments": len(apps_v1.list_deployment_for_all_namespaces().items),
            "services": len(v1.list_service_for_all_namespaces().items),
            "daemonsets": len(apps_v1.list_daemon_set_for_all_namespaces().items),
            "jobs": len(batch_v1.list_job_for_all_namespaces().items),
            "cronjobs": len(batch_v1.list_cron_job_for_all_namespaces().items),
            "ingresses": len(networking_v1.list_ingress_for_all_namespaces().items)
        }
        return cluster_info
    except Exception as e:
        print(f"Error fetching cluster info: {e}")
    
    return None

def get_deployments(namespace=None):
    load_kube_config()
    v1 = client.AppsV1Api()
    if namespace:
        deployments = v1.list_namespaced_deployment(namespace).items
    else:
        deployments = v1.list_deployment_for_all_namespaces().items
    return [deployment.metadata.name for deployment in deployments]

def get_services(namespace=None):
    load_kube_config()
    v1 = client.CoreV1Api()
    if namespace:
        services = v1.list_namespaced_service(namespace).items
    else:
        services = v1.list_service_for_all_namespaces().items
    return [service.metadata.name for service in services]

def get_daemonsets(namespace=None):
    load_kube_config()
    v1 = client.AppsV1Api()
    if namespace:
        daemonsets = v1.list_namespaced_daemon_set(namespace).items
    else:
        daemonsets = v1.list_daemon_set_for_all_namespaces().items
    return [daemonset.metadata.name for daemonset in daemonsets]

def get_ingresses(namespace=None):
    load_kube_config()
    v1 = client.NetworkingV1Api()
    if namespace:
        ingresses = v1.list_namespaced_ingress(namespace).items
    else:
        ingresses = v1.list_ingress_for_all_namespaces().items
    return [ingress.metadata.name for ingress in ingresses]

def get_jobs(namespace=None):
    load_kube_config()
    v1 = client.BatchV1Api()
    if namespace:
        jobs = v1.list_namespaced_job(namespace).items
    else:
        jobs = v1.list_job_for_all_namespaces().items
    return [job.metadata.name for job in jobs]

