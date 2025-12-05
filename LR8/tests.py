import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from myapp.models import Author, User, Currency, UserCurrency
from myapp.utils.currencies_api import get_currencies


class TestModels(unittest.TestCase):
    """Тесты для моделей предметной области."""

    def test_author_valid(self) -> None:
        author = Author("Миша", "P3122")
        self.assertEqual(author.name, "Миша")
        self.assertEqual(author.group, "P3122")

    def test_user_id_positive(self) -> None:
        # id не может быть нулевым или отрицательным
        with self.assertRaises(ValueError):
            User(0, "Имя")

    def test_currency_value_positive(self) -> None:
        c = Currency("R0000", 1, "AAA", "Тест", 10.0, 1)
        self.assertEqual(c.value, 10.0)
        # отрицательное значение курса запрещено
        with self.assertRaises(ValueError):
            c.value = -5

    def test_user_currency_links(self) -> None:
        uc = UserCurrency(1, 2, "R0000")
        self.assertEqual(uc.user_id, 2)
        self.assertEqual(uc.currency_id, "R0000")


class TestCurrenciesApi(unittest.TestCase):
    """Тесты для функции get_currencies."""

    def test_get_currencies_returns_list_or_skip(self) -> None:
        """
        Проверяем, что get_currencies возвращает список валют.
        Если API ЦБ недоступно, тест помечается как пропущенный.
        """
        try:
            result = get_currencies()
        except RuntimeError:
            self.skipTest("API ЦБ РФ недоступно")
            return

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], Currency)


if __name__ == "__main__":
    unittest.main()
