import os
import sys
import unittest
from types import SimpleNamespace

from pydantic import ValidationError


os.environ.setdefault("SECRET_KEY", "test-secret")
sys.path.insert(0, os.path.abspath("backend"))

from app.core.security import ALGORITHM, SECRET_KEY, create_access_token, hash_password, verify_password
from app.services.schemas.guarantee import GuaranteeCreate
from app.services.schemas.order import OrderCreate
from app.services.schemas.user_schemas import UserCreate, UserPublic
from dependency import get_current_user
from jose import jwt


class SchemaValidationTests(unittest.TestCase):
    """Автотесты валидации входных и выходных Pydantic-схем."""

    def test_user_create_trims_username_and_password(self):
        """Пробелы по краям логина и пароля должны удаляться валидаторами."""
        user = UserCreate(username="  tester  ", password="  secret1  ")

        self.assertEqual(user.username, "tester")
        self.assertEqual(user.password, "secret1")

    def test_user_create_rejects_short_values(self):
        """Короткие логин и пароль должны отклоняться."""
        with self.assertRaises(ValidationError):
            UserCreate(username="ab", password="123")

    def test_user_public_rejects_empty_role(self):
        """Публичная модель пользователя не должна принимать пустую роль."""
        with self.assertRaises(ValidationError):
            UserPublic(username="tester", user_role=" ")

    def test_order_create_requires_components_and_positive_warranty(self):
        """Создание заказа требует хотя бы один компонент и положительную гарантию."""
        valid = OrderCreate(component_ids=[1, 2], warranty_period=12)
        self.assertEqual(valid.component_ids, [1, 2])

        with self.assertRaises(ValidationError):
            OrderCreate(component_ids=[], warranty_period=12)
        with self.assertRaises(ValidationError):
            OrderCreate(component_ids=[1], warranty_period=0)

    def test_guarantee_create_limits_problem_description(self):
        """Гарантийное обращение должно иметь содержательное описание проблемы."""
        with self.assertRaises(ValidationError):
            GuaranteeCreate(order_id=1, defective_component_id=2, problem_description="коротко")


class SecurityTests(unittest.TestCase):
    """Автотесты хеширования паролей и JWT-аутентификации."""

    def test_password_hash_is_not_plain_text_and_verifies(self):
        """Пароль должен храниться как bcrypt-хеш и проходить проверку только с верным значением."""
        hashed = hash_password("secret-password")

        self.assertNotEqual(hashed, "secret-password")
        self.assertTrue(verify_password("secret-password", hashed))
        self.assertFalse(verify_password("wrong-password", hashed))

    def test_access_token_contains_user_identity(self):
        """JWT должен содержать имя, роль, id пользователя и срок действия."""
        token = create_access_token(username="tester", user_role="customer", user_id=42)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        self.assertEqual(payload["sub"], "tester")
        self.assertEqual(payload["user_role"], "customer")
        self.assertEqual(payload["user_id"], 42)
        self.assertIn("exp", payload)

    def test_get_current_user_extracts_payload(self):
        """Dependency текущего пользователя должен возвращать данные из Bearer-токена."""
        token = create_access_token(username="importer", user_role="importer", user_id=7)
        current_user = get_current_user(SimpleNamespace(credentials=token))

        self.assertEqual(
            current_user,
            {"username": "importer", "role": "importer", "user_id": 7},
        )


if __name__ == "__main__":
    unittest.main()
