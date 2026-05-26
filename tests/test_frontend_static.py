import os
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JS_DIR = ROOT / "frontend" / "static" / "js"
TEMPLATES_DIR = ROOT / "frontend" / "templates"


class FrontendStaticTests(unittest.TestCase):
    """Статические автотесты доступности frontend-страниц и JS-функций."""

    def test_required_templates_exist(self):
        """Ключевые HTML-страницы пользовательских сценариев должны быть в проекте."""
        required = [
            "login.html",
            "registration.html",
            "create-pc.html",
            "orders.html",
            "available_orders.html",
            "my_guarantees.html",
            "personal_account.html",
        ]

        for name in required:
            with self.subTest(template=name):
                self.assertTrue((TEMPLATES_DIR / name).exists())

    def test_utils_declares_order_and_guarantee_functions(self):
        """Общие JS-функции заказов и гарантий должны присутствовать во frontend."""
        text = (JS_DIR / "utils.js").read_text(encoding="utf-8")
        functions = [
            "parseJwt",
            "takeOrder",
            "changeStatus",
            "openGuaranteeModal",
            "closeGuaranteeModal",
            "submitGuarantee",
        ]

        for name in functions:
            with self.subTest(function=name):
                self.assertRegex(text, rf"function\s+{re.escape(name)}\s*\(")

    def test_frontend_scripts_use_api_v1_prefix(self):
        """Frontend должен обращаться к актуальному префиксу API /api/v1."""
        scripts = [path for path in JS_DIR.glob("*.js") if path.is_file()]

        self.assertTrue(scripts)
        self.assertTrue(any("/api/v1/" in path.read_text(encoding="utf-8") for path in scripts))


if __name__ == "__main__":
    unittest.main()
