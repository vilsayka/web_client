import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch


os.environ.setdefault("SECRET_KEY", "test-secret")
sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient

import dependency
from app.core.security import create_access_token
from main import app


def fake_db():
    yield object()


def fake_customer():
    return {"username": "customer", "role": "customer", "user_id": 5}


def fake_importer():
    return {"username": "importer", "role": "importer", "user_id": 8}


class ApiTests(unittest.TestCase):
    """Автотесты публичных API endpoint без подключения к реальной БД."""

    def setUp(self):
        app.dependency_overrides[dependency.get_db_master] = fake_db
        app.dependency_overrides[dependency.get_db_slave] = fake_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    @patch("app.api.v1.endpoints.auth.authenticate")
    def test_login_returns_bearer_token(self, authenticate_mock):
        """POST /api/v1/login возвращает Bearer-токен для валидных учетных данных."""
        authenticate_mock.return_value = {"user_name": "tester", "user_role": "customer", "id_user": 42}

        response = self.client.post(
            "/api/v1/login",
            data={"username": "tester", "password": "secret"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")

    @patch("app.api.v1.endpoints.auth.authenticate", return_value=None)
    def test_login_rejects_bad_credentials(self, _):
        """POST /api/v1/login возвращает 401 при неверных учетных данных."""
        response = self.client.post(
            "/api/v1/login",
            data={"username": "tester", "password": "wrong"},
        )

        self.assertEqual(response.status_code, 401)

    def test_refresh_returns_new_token(self):
        """POST /api/v1/refresh обновляет валидный Bearer-токен."""
        token = create_access_token("tester", "customer", 42)

        response = self.client.post("/api/v1/refresh", headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    @patch("app.api.v1.endpoints.components.get_all_components_grouped")
    def test_components_endpoint_returns_grouped_components(self, grouped_mock):
        """GET /api/v1/components/ возвращает сгруппированный список комплектующих."""
        grouped_mock.return_value = {"components": [{"category": "Процессор", "items": []}]}

        response = self.client.get("/api/v1/components/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["components"][0]["category"], "Процессор")

    @patch("app.api.v1.endpoints.build.get_component")
    def test_build_check_returns_conflicts(self, get_component_mock):
        """POST /api/v1/build/check возвращает совместимость и список конфликтов."""
        data = {
            1: {"title": "Processor", "specifications": {"socket": "AM5"}},
            2: {"title": "Motherboard", "specifications": {"socket": "LGA1700"}},
        }
        get_component_mock.side_effect = lambda _, cid: data[cid]

        response = self.client.post("/api/v1/build/check", json={"component_ids": [1, 2]})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["compatible"])
        self.assertTrue(response.json()["conflicts"])

    @patch("app.api.v1.endpoints.orders.get_available_orders")
    def test_available_orders_allowed_for_importer(self, available_mock):
        """GET /api/v1/orders/available доступен только роли importer."""
        app.dependency_overrides[dependency.get_current_user] = fake_importer
        available_mock.return_value = [
            {
                "id_order": 1,
                "id_customer": 5,
                "customer_name": "customer",
                "status_order": "ожидает сборщика",
                "warranty_period": 12,
                "created_at": datetime(2026, 1, 1),
            }
        ]

        response = self.client.get("/api/v1/orders/available")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["id_order"], 1)

    def test_available_orders_forbidden_for_customer(self):
        """GET /api/v1/orders/available запрещен роли customer."""
        app.dependency_overrides[dependency.get_current_user] = fake_customer

        response = self.client.get("/api/v1/orders/available")

        self.assertEqual(response.status_code, 403)

    @patch("app.api.v1.endpoints.guarantees.create_guarantee")
    def test_create_guarantee_request_for_customer(self, create_mock):
        """POST /api/v1/guarantees/ создает гарантийное обращение клиента."""
        app.dependency_overrides[dependency.get_current_user] = fake_customer
        create_mock.return_value = {
            "id_repair_warranty": 1,
            "id_order": 10,
            "id_defective_component": 2,
            "date_references": "2026-05-26",
            "problem_description": "Компьютер не включается после сборки",
            "status_repair": "создано",
            "created_at": "2026-05-26T10:00:00",
            "date_repair_completion": None,
        }

        response = self.client.post(
            "/api/v1/guarantees/",
            json={
                "order_id": 10,
                "defective_component_id": 2,
                "problem_description": "Компьютер не включается после сборки",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id_repair_warranty"], 1)


if __name__ == "__main__":
    unittest.main()
