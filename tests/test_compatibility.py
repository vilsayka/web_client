import os
import sys
import unittest


os.environ.setdefault("SECRET_KEY", "test-secret")
sys.path.insert(0, os.path.abspath("backend"))

from app.services.compatibility import get_category, perform_compatibility_check


def component(title, **specifications):
    return {"title": title, "specifications": specifications}


class CompatibilityTests(unittest.TestCase):
    """Автотесты правил совместимости комплектующих."""

    def test_get_category_returns_known_internal_category(self):
        """Компонент с известным title должен попадать во внутреннюю категорию."""
        self.assertEqual(get_category(component("Processor")), "processor")
        self.assertEqual(get_category(component("Graphics Card")), "gpu")

    def test_compatible_full_build_has_no_conflicts(self):
        """Согласованная сборка не должна возвращать конфликты."""
        build = [
            component("Processor", socket="AM5", tdp_w=120),
            component("Motherboard", socket="AM5", ram_type="DDR5", form_factor="ATX"),
            component("RAM", type="DDR5"),
            component("CPU Cooler", supported_sockets=["AM5"], tdp_w=220),
            component("Graphics Card", tdp_w=250),
            component("Power Supply", wattage=750),
            component("Case", form_factors_supported=["ATX", "mATX"]),
        ]

        self.assertEqual(perform_compatibility_check(build), [])

    def test_detects_socket_ram_case_psu_and_duplicate_conflicts(self):
        """Проверка должна находить ключевые конфликты сборки."""
        build = [
            component("Processor", socket="AM5", tdp_w=170),
            component("Processor", socket="AM5", tdp_w=170),
            component("Motherboard", socket="LGA1700", ram_type="DDR5", form_factor="E-ATX"),
            component("RAM", type="DDR4"),
            component("CPU Cooler", supported_sockets=["LGA1700"], tdp_w=120),
            component("Graphics Card", tdp_w=450),
            component("Power Supply", wattage=500),
            component("Case", form_factors_supported=["ATX", "mATX"]),
            component("Sound Card"),
        ]

        conflicts = perform_compatibility_check(build)

        self.assertGreaterEqual(len(conflicts), 7)
        self.assertTrue(any("Дублирование" in item for item in conflicts))
        self.assertTrue(any("Сокет" in item for item in conflicts))
        self.assertTrue(any("Кулер" in item for item in conflicts))
        self.assertTrue(any("памяти" in item for item in conflicts))
        self.assertTrue(any("Форм-фактор" in item for item in conflicts))
        self.assertTrue(any("Блок питания" in item for item in conflicts))
        self.assertTrue(any("Неизвестный тип" in item for item in conflicts))


if __name__ == "__main__":
    unittest.main()
