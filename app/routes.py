from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.k8s_client import (
    create_namespace,
    get_daemonsets,
    get_deployments,
    get_namespaces,
    get_nodes,
    get_pods,
    get_services,
    get_ingresses,
    get_jobs,
    get_cluster_info,
)

router = APIRouter()


def configure_routes(app: FastAPI):
    @router.get("/cluster-info", response_class=JSONResponse, tags=["cluster info"])
    def cluster_info():
        try:
            cluster_name = get_cluster_info()
            return JSONResponse(content=cluster_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/daemonsets", response_class=JSONResponse, tags=["daemonsets"])
    def daemonsets_in_all_namespaces():
        try:
            daemonsets_data = get_daemonsets()
            return JSONResponse(content=daemonsets_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/daemonsets/{namespace}", response_class=JSONResponse, tags=["daemonsets"])
    def daemonsets_in_namespace(namespace: str):
        try:
            daemonsets_data = get_daemonsets(namespace)
            return JSONResponse(content=daemonsets_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/deployments", response_class=JSONResponse, tags=["deployments"])
    def deployments_in_all_namespaces():
        try:
            deployment_data = get_deployments()
            return JSONResponse(content=deployment_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/deployments/{namespace}", response_class=JSONResponse, tags=["deployments"])
    def deployments_in_namespace(namespace: str):
        try:
            deployment_data = get_deployments(namespace)
            return JSONResponse(content=deployment_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/ingresses", response_class=JSONResponse, tags=["ingresses"])
    def ingresses_in_all_namespaces():
        try:
            ingress_data = get_ingresses()
            return JSONResponse(content=ingress_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/ingresses/{namespace}", response_class=JSONResponse, tags=["ingresses"])
    def ingresses_in_namespace(namespace: str):
        try:
            ingress_data = get_deployments(namespace)
            return JSONResponse(content=ingress_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/jobs", response_class=JSONResponse, tags=["jobs"])
    def jobs_in_all_namespaces():
        try:
            jobs_data = get_jobs()
            return JSONResponse(content=jobs_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/jobs_data/{namespace}", response_class=JSONResponse, tags=["jobs"])
    def jobs_in_namespace(namespace: str):
        try:
            jobs_data = get_jobs(namespace)
            return JSONResponse(content=jobs_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/namespaces", response_class=JSONResponse, tags=["namespaces"])
    def namespaces():
        try:
            namespaces_data = get_namespaces()
            return JSONResponse(content=namespaces_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/namespace/{name}", response_class=JSONResponse, tags=["namespaces"])
    def create_ns(name: str):
        try:
            create_namespace(name)
            return JSONResponse(content={"message": f"Namespace '{name}' created."})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/nodes", response_class=JSONResponse, tags=["nodes"])
    def nodes():
        try:
            nodes_data = get_nodes()
            return JSONResponse(content=nodes_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/pods", response_class=JSONResponse, tags=["pods"])
    def all_pods():
        try:
            pods_data = get_pods()
            return JSONResponse(content=pods_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/pods/{namespace}", response_class=JSONResponse, tags=["pods"])
    def pods_in_namespace(namespace: str):
        try:
            pods_data = get_pods(namespace)
            return JSONResponse(content=pods_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/services", response_class=JSONResponse, tags=["services"])
    def serices_in_all_namespaces():
        try:
            service_data = get_services()
            return JSONResponse(content=service_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/services/{namespace}", response_class=JSONResponse, tags=["services"])
    def services_in_namespace(namespace: str):
        try:
            service_data = get_services(namespace)
            return JSONResponse(content=service_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    app.include_router(router)
