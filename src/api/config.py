import os


class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    KUBECONFIG = os.getenv("KUBECONFIG", "")
    CLUSTER_URL = os.getenv("CLUSTER_URL", "")
    CLUSTER_AUTH_TOKEN = os.getenv("CLUSTER_AUTH_TOKEN", "")
