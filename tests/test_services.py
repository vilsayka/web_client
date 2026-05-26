import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from fastapi import HTTPException


os.environ.setdefault("SECRET_KEY", "test-secret")
sys.path.insert(0, os.path.abspath("backend"))

from app.services import component_service, guarantee_service, order_service, user_service


COMPONENT = {
    "id_component": 1,
    "title": "Processor",
    "manufacturer": "AMD",
    "model": "Ryzen",
    "price_complete": 10000.0,
    "specifications": {"socket": "AM5", "cores": 8},
}


class ComponentServiceTests(unittest.TestCase):
    """Автотесты сервисного слоя комплектующих."""

    @patch("app.services.component_service.component_repo.get_components_by_title")
    def test_get_components_by_category_maps_russian_category(self, repo_mock):
        """Русская категория должна преобразовываться в title компонента из БД."""
        repo_mock.return_value = [COMPONENT]

        result = component_service.get_components_by_category(MagicMock(), "Процессор")

        repo_mock.assert_called_once()
        self.assertEqual(result[0]["name"], "AMD Ryzen")
        self.assertIn("сокет AM5", result[0]["description"])

    def test_get_components_by_category_rejects_unknown_category(self):
        """Неизвестная категория должна возвращать HTTP 400."""
        with self.assertRaises(HTTPException) as ctx:
            component_service.get_components_by_category(MagicMock(), "Монитор")

        self.assertEqual(ctx.exception.status_code, 400)

    @patch("app.services.component_service.component_repo.get_all_components")
    def test_get_all_components_grouped_returns_frontend_shape(self, repo_mock):
        """Группировка должна возвращать формат, ожидаемый фронтендом."""
        repo_mock.return_value = [COMPONENT]

        result = component_service.get_all_components_grouped(MagicMock())

        self.assertEqual(result["components"][0]["category"], "Процессор")
        self.assertEqual(result["components"][0]["items"][0]["id"], 1)


class OrderServiceTests(unittest.TestCase):
    """Автотесты бизнес-логики заказов."""

    @patch("app.services.order_service.add_components_to_order")
    @patch("app.services.order_service.repo_create_order")
    @patch("app.services.order_service.component_repo.get_component")
    def test_create_order_validates_components_and_adds_them(self, get_component, create_order, add_components):
        """Заказ создается только после проверки существования всех компонентов."""
        get_component.return_value = COMPONENT
        create_order.return_value = {
            "id_order": 10,
            "id_customer": 5,
            "id_importer": None,
            "status_order": "ожидает сборщика",
            "warranty_period": 12,
            "created_at": datetime(2026, 1, 1),
        }

        result = order_service.create_order(MagicMock(), 5, [1, 2], 12)

        self.assertEqual(result["id_order"], 10)
        add_components.assert_called_once_with(unittest.mock.ANY, 10, [1, 2])

    @patch("app.services.order_service.component_repo.get_component", return_value=None)
    def test_create_order_returns_404_for_missing_component(self, _):
        """Если компонент не найден, заказ не должен создаваться."""
        with self.assertRaises(HTTPException) as ctx:
            order_service.create_order(MagicMock(), 5, [999], 12)

        self.assertEqual(ctx.exception.status_code, 404)

    @patch("app.services.order_service.get_order_components")
    @patch("app.services.order_service.get_order_by_id")
    def test_get_order_details_calculates_total_price(self, order_mock, components_mock):
        """Детали заказа должны включать состав и итоговую стоимость."""
        order_mock.return_value = {
            "id_order": 10,
            "id_customer": 5,
            "id_importer": 8,
            "status_order": "собрана",
            "date_assembly": None,
            "warranty_period": 12,
            "created_at": datetime(2026, 1, 1),
        }
        components_mock.return_value = [{"price": 100.0, "quantity": 2}, {"price": 50.0, "quantity": 1}]

        result = order_service.get_order_details(MagicMock(), 10)

        self.assertEqual(result["total_price"], 250.0)
        self.assertEqual(len(result["components"]), 2)

    @patch("app.services.order_service.get_order_details")
    @patch("app.services.order_service.update_order_status", return_value=True)
    @patch("app.services.order_service.get_order_by_id")
    def test_change_order_status_allows_valid_transition(self, order_mock, update_mock, details_mock):
        """Сборщик может перевести свой заказ по разрешенной цепочке статусов."""
        order_mock.return_value = {"id_importer": 8, "status_order": "ожидает сборщика"}
        details_mock.return_value = {"id_order": 10, "status_order": "на сборке"}

        result = order_service.change_order_status(MagicMock(), 10, 8, "на сборке")

        self.assertEqual(result["status_order"], "на сборке")
        update_mock.assert_called_once()

    @patch("app.services.order_service.get_order_by_id")
    def test_change_order_status_rejects_foreign_order(self, order_mock):
        """Сборщик не может менять статус чужого заказа."""
        order_mock.return_value = {"id_importer": 99, "status_order": "на сборке"}

        with self.assertRaises(HTTPException) as ctx:
            order_service.change_order_status(MagicMock(), 10, 8, "собрана")

        self.assertEqual(ctx.exception.status_code, 403)


class UserAndGuaranteeServiceTests(unittest.TestCase):
    """Автотесты пользователей и гарантийных обращений."""

    @patch("app.services.user_service.get_user")
    @patch("app.services.user_service.verify_password", return_value=True)
    def test_authenticate_returns_user_for_valid_password(self, _, get_user):
        """Пользователь должен авторизоваться при верном пароле."""
        get_user.return_value = {"user_name": "tester", "password_hash": "hash"}

        self.assertEqual(user_service.authenticate(MagicMock(), "tester", "secret")["user_name"], "tester")

    @patch("app.services.guarantee_service.repo_create_guarantee")
    @patch("app.services.guarantee_service.get_order_components")
    @patch("app.services.guarantee_service.get_order_by_id")
    def test_create_guarantee_for_completed_own_order(self, order_mock, components_mock, create_mock):
        """Клиент может создать гарантийное обращение по своему завершенному заказу."""
        order_mock.return_value = {"id_customer": 5, "status_order": "собрана"}
        components_mock.return_value = [{"id_component": 1}]
        create_mock.return_value = {"id_repair_warranty": 3}

        result = guarantee_service.create_guarantee(
            MagicMock(),
            5,
            {"order_id": 10, "defective_component_id": 1, "problem_description": "Не включается"},
        )

        self.assertEqual(result["id_repair_warranty"], 3)

    @patch("app.services.guarantee_service.get_order_by_id")
    def test_create_guarantee_rejects_foreign_order(self, order_mock):
        """Клиент не может завести гарантию по чужому заказу."""
        order_mock.return_value = {"id_customer": 99, "status_order": "собрана"}

        with self.assertRaises(HTTPException) as ctx:
            guarantee_service.create_guarantee(
                MagicMock(),
                5,
                {"order_id": 10, "defective_component_id": 1, "problem_description": "Не включается"},
            )

        self.assertEqual(ctx.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
