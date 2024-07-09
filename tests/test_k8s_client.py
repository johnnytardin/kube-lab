import pytest
from unittest.mock import patch, MagicMock
from src.api.k8s_client import (
    load_kube_config, get_nodes, get_namespaces, create_namespace,
    get_pods, get_cluster_info, get_deployments, get_services,
    get_daemonsets, get_ingresses, get_jobs
)
from src.api.config import Config


@patch('src.api.k8s_client.config.load_kube_config')
@patch('src.api.k8s_client.config.load_kube_config_from_dict')
@patch('builtins.open', new_callable=MagicMock)
@patch('src.api.k8s_client.yaml.safe_load')
def test_load_kube_config(mock_safe_load, mock_open, mock_load_from_dict, mock_load_kube_config):
    mock_safe_load.return_value = {
        "clusters": [{"cluster": {"server": "original-server-url"}}]
    }
    Config.CLUSTER_URL = "mock-cluster-url"
    Config.KUBECONFIG = "mock-kubeconfig"

    load_kube_config()

    mock_open.assert_called_once_with(Config.KUBECONFIG, "r")
    mock_safe_load.assert_called_once()
    mock_load_from_dict.assert_called_once()
    mock_load_kube_config.assert_not_called()

@patch('src.api.k8s_client.client.CoreV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_nodes(mock_load_kube_config, mock_CoreV1Api):
    mock_api_instance = mock_CoreV1Api.return_value
    mock_node = MagicMock()
    mock_node.metadata.name = "node1"
    mock_api_instance.list_node.return_value.items = [mock_node]
    
    nodes = get_nodes()    
    mock_load_kube_config.assert_called_once()    
    mock_api_instance.list_node.assert_called_once()
    
    assert nodes == ["node1"]

@patch('src.api.k8s_client.client.CoreV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_namespaces(mock_load_kube_config, mock_CoreV1Api):
    mock_api_instance = mock_CoreV1Api.return_value
    mock_namespace = MagicMock(metadata=MagicMock(name="namespace1"))
    mock_api_instance.list_namespace.return_value.items = [mock_namespace]
    
    namespaces = get_namespaces()
    
    mock_load_kube_config.assert_called_once()
    mock_api_instance.list_namespace.assert_called_once()
    assert namespaces == [mock_namespace.metadata.name]

@patch('src.api.k8s_client.client.CoreV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_create_namespace(mock_load_kube_config, mock_CoreV1Api):
    mock_api_instance = mock_CoreV1Api.return_value
    namespace_name = "test-namespace"
    
    create_namespace(namespace_name)
    
    mock_load_kube_config.assert_called_once()
    mock_api_instance.create_namespace.assert_called_once()

@patch('src.api.k8s_client.client.CoreV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_pods(mock_load_kube_config, mock_CoreV1Api):
    mock_api_instance = mock_CoreV1Api.return_value
    mock_pods = MagicMock()
    mock_pods.metadata.name = "pod1"
    mock_api_instance.list_pod_for_all_namespaces.return_value.items = [mock_pods]
    
    pods = get_pods()
    
    mock_load_kube_config.assert_called_once()
    mock_api_instance.list_pod_for_all_namespaces.assert_called_once()
    assert pods == ["pod1"]

@patch('src.api.k8s_client.client.CoreV1Api')
@patch('src.api.k8s_client.client.AppsV1Api')
@patch('src.api.k8s_client.client.BatchV1Api')
@patch('src.api.k8s_client.client.NetworkingV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_cluster_info(mock_load_kube_config, mock_CoreV1Api, mock_AppsV1Api, mock_BatchV1Api, mock_NetworkingV1Api):
    mock_v1_instance = mock_CoreV1Api.return_value
    mock_apps_v1_instance = mock_AppsV1Api.return_value
    mock_batch_v1_instance = mock_BatchV1Api.return_value
    mock_networking_v1_instance = mock_NetworkingV1Api.return_value

    mock_v1_instance.list_node.return_value.items = [MagicMock()]
    mock_v1_instance.list_namespace.return_value.items = [MagicMock()]
    mock_v1_instance.list_pod_for_all_namespaces.return_value.items = [MagicMock()]
    mock_v1_instance.list_service_for_all_namespaces.return_value.items = [MagicMock()]
    mock_apps_v1_instance.list_deployment_for_all_namespaces.return_value.items = [MagicMock()]
    mock_apps_v1_instance.list_daemon_set_for_all_namespaces.return_value.items = [MagicMock()]
    mock_batch_v1_instance.list_job_for_all_namespaces.return_value.items = [MagicMock()]
    mock_batch_v1_instance.list_cron_job_for_all_namespaces.return_value.items = [MagicMock()]
    mock_networking_v1_instance.list_ingress_for_all_namespaces.return_value.items = [MagicMock()]

    cluster_info = get_cluster_info()

    mock_load_kube_config.assert_called_once()
    assert cluster_info == {
        "nodes": 0,
        "namespaces": 0,
        "pods": 0,
        "deployments": 0,
        "services": 0,
        "daemonsets": 0,
        "jobs": 0,
        "cronjobs": 0,
        "ingresses": 0,
    }

@patch('src.api.k8s_client.client.AppsV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_deployments(mock_load_kube_config, mock_AppsV1Api):
    mock_api_instance = mock_AppsV1Api.return_value
    mock_deployment = MagicMock()
    mock_deployment.metadata.name = "deployment1"
    mock_api_instance.list_deployment_for_all_namespaces.return_value.items = [mock_deployment]
    
    deployments = get_deployments()
    
    mock_load_kube_config.assert_called_once()
    mock_api_instance.list_deployment_for_all_namespaces.assert_called_once()
    assert deployments == ["deployment1"]

@patch('src.api.k8s_client.client.CoreV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_services(mock_load_kube_config, mock_CoreV1Api):
    mock_api_instance = mock_CoreV1Api.return_value
    mock_service = MagicMock()
    mock_service.metadata.name = "service1"
    mock_api_instance.list_service_for_all_namespaces.return_value.items = [mock_service]
    
    services = get_services()
    
    mock_load_kube_config.assert_called_once()
    mock_api_instance.list_service_for_all_namespaces.assert_called_once()
    assert services == ["service1"]

@patch('src.api.k8s_client.client.AppsV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_daemonsets(mock_load_kube_config, mock_AppsV1Api):
    mock_api_instance = mock_AppsV1Api.return_value
    mock_daemoset = MagicMock()
    mock_daemoset.metadata.name = "daemonset1"
    mock_api_instance.list_daemon_set_for_all_namespaces.return_value.items = [mock_daemoset]
    
    daemonsets = get_daemonsets()
    
    mock_load_kube_config.assert_called_once()
    mock_api_instance.list_daemon_set_for_all_namespaces.assert_called_once()
    assert daemonsets == ["daemonset1"]

@patch('src.api.k8s_client.client.NetworkingV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_ingresses(mock_load_kube_config, mock_NetworkingV1Api):
    mock_api_instance = mock_NetworkingV1Api.return_value
    mock_ingress = MagicMock()
    mock_ingress.metadata.name = "ingress1"
    mock_api_instance.list_ingress_for_all_namespaces.return_value.items = [mock_ingress]
       
    ingresses = get_ingresses()
    
    mock_load_kube_config.assert_called_once()
    mock_api_instance.list_ingress_for_all_namespaces.assert_called_once()
    assert ingresses == ["ingress1"]

@patch('src.api.k8s_client.client.BatchV1Api')
@patch('src.api.k8s_client.load_kube_config')
def test_get_jobs(mock_load_kube_config, mock_BatchV1Api):
    mock_api_instance = mock_BatchV1Api.return_value
    mock_api_instance.list_job_for_all_namespaces.return_value.items = [MagicMock(metadata=MagicMock(name="job1"))]
    
    jobs = get_jobs()
    
    mock_load_kube_config.assert_called