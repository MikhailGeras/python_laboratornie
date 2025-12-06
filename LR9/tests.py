import sys
from pathlib import Path
import unittest

BASE_DIR = Path(__file__).resolve().parent  # .../LR9
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from myapp.controllers.databasecontroller import DatabaseController
from myapp.controllers.currencycontroller import CurrencyController


class TestCurrencyController(unittest.TestCase):
    """Тесты для контроллера валют на реальной базе SQLite (:memory:)."""

    def setUp(self) -> None:
        """Создаём новую БД в памяти и контроллер перед каждым тестом."""
        self.db = DatabaseController()
        self.controller = CurrencyController(self.db)

    def test_list_currencies_returns_non_empty_list(self) -> None:
        """При запуске в таблице currency должны быть стартовые данные."""
        currencies = self.controller.list_currencies()

        # Проверяем, что список не пустой и в записи есть ожидаемые поля.
        self.assertGreater(len(currencies), 0)
        first = currencies[0]
        self.assertIn("id", first)
        self.assertIn("char_code", first)
        self.assertIn("value", first)

    def test_update_currency_changes_value(self) -> None:
        """Обновление курса валюты должно менять значение в таблице."""
        currencies_before = self.controller.list_currencies()
        first = currencies_before[0]
        code = first["char_code"]
        old_value = float(first["value"])

        new_value = old_value + 1.0
        self.controller.update_currencies({code: new_value})

        currencies_after = self.controller.list_currencies()
        updated = next(c for c in currencies_after if c["char_code"] == code)

        self.assertEqual(float(updated["value"]), new_value)

    def test_delete_currency_reduces_count(self) -> None:
        """Удаление валюты должно уменьшать количество записей."""
        currencies_before = self.controller.list_currencies()
        count_before = len(currencies_before)
        currency_id = currencies_before[0]["id"]

        self.controller.delete_currency(int(currency_id))

        currencies_after = self.controller.list_currencies()
        count_after = len(currencies_after)

        self.assertEqual(count_after, count_before - 1)


if __name__ == "__main__":
    unittest.main()
