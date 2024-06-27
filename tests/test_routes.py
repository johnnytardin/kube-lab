import unittest
import string
import random

from fastapi.testclient import TestClient
from app import create_app

app = create_app()

class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.test_namespace = "".join(random.choices(string.ascii_lowercase, k=10))

    def test_nodes(self):
        response = self.client.get("/nodes")
        self.assertEqual(response.status_code, 200)

    def test_namespaces(self):
        response = self.client.get("/namespaces")
        self.assertEqual(response.status_code, 200)

    def test_create_namespace(self):
        created = self.client.post(f"/namespace/{self.test_namespace}")
        self.assertEqual(created.status_code, 200)
        self.assertEqual(
            created.json(), {"message": f"Namespace '{self.test_namespace}' created."}
        )

        response = self.client.get("/namespaces")
        self.assertIn(self.test_namespace, response.json())

    def test_pods_in_namespace(self):
        response = self.client.get("/pods/default")
        self.assertEqual(response.status_code, 200)

    def test_all_pods(self):
        response = self.client.get("/pods")
        self.assertEqual(response.status_code, 200)

    def test_deployments_in_all_namespaces(self):
        response = self.client.get("/deployments")
        self.assertEqual(response.status_code, 200)

    def test_deployments_in_namespace(self):
        response = self.client.get("/deployments/default")
        self.assertEqual(response.status_code, 200)

    def test_ingresses_in_all_namespaces(self):
        response = self.client.get("/ingresses")
        self.assertEqual(response.status_code, 200)

    def test_ingresses_in_namespace(self):
        response = self.client.get("/ingresses/default")
        self.assertEqual(response.status_code, 200)

    def test_jobs_in_all_namespaces(self):
        response = self.client.get("/jobs")
        self.assertEqual(response.status_code, 200)

    def test_jobs_in_namespace(self):
        response = self.client.get("/jobs/default")
        self.assertEqual(response.status_code, 200)

    def test_daemonsets_in_all_namespaces(self):
        response = self.client.get("/daemonsets")
        self.assertEqual(response.status_code, 200)

    def test_daemonsets_in_namespace(self):
        response = self.client.get("/daemonsets/default")
        self.assertEqual(response.status_code, 200)

    def test_services_in_all_namespaces(self):
        response = self.client.get("/services")
        self.assertEqual(response.status_code, 200)

    def test_services_in_namespace(self):
        response = self.client.get("/services/default")
        self.assertEqual(response.status_code, 200)
