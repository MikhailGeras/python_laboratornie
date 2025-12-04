import unittest
import io
import sys

from main import (
    logger,
    get_currencies,
)


class TestGetCurrencies(unittest.TestCase):

    def test_currency_usd_ok(self):
        """
        Проверяем, что USD возвращается и курс выглядит разумно.
        """
        data = get_currencies(["USD"])
        self.assertIn("USD", data)
        self.assertIsInstance(data["USD"], (int, float))
        self.assertGreater(data["USD"], 0)
        self.assertLess(data["USD"], 1000)

    def test_missing_currency_raises_keyerror(self):
        """
        Если передать несуществующую валюту, должен быть KeyError.
        """
        with self.assertRaises(KeyError):
            get_currencies(["ZZZ"])

    def test_connection_error(self):
        """
        При неправильном URL ожидаем ConnectionError.
        """
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://invalid-url-for-test")

    def test_invalid_json_raises_valueerror(self):
        """
        При корректном HTTP, но некорректном JSON ожидаем ValueError.
        example.com возвращает HTML, а не JSON.
        """
        with self.assertRaises(ValueError):
            get_currencies(["USD"], url="https://example.com/")



class TestLoggerWithStringIO(unittest.TestCase):

    def setUp(self):
        # каждый тест будет использовать свой поток в памяти
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def success_func(x):
            return x * 2

        @logger(handle=self.stream)
        def fail_func():
            raise ValueError("boom")

        self.success_func = success_func
        self.fail_func = fail_func

    def test_logging_success(self):
        """
        При успешном выполнении:
        - должны быть записи с INFO
        - должен быть залогирован возврат значения
        """
        result = self.success_func(10)
        self.assertEqual(result, 20)

        logs = self.stream.getvalue()
        self.assertIn("INFO:", logs)
        self.assertIn("Calling success_func", logs)
        self.assertIn("returned 20", logs)

    def test_logging_error(self):
        """
        При ошибке:
        - должно быть слово ERROR в логах
        - исключение должно пробрасываться дальше
        """
        with self.assertRaises(ValueError):
            self.fail_func()

        logs = self.stream.getvalue()
        self.assertIn("ERROR:", logs)
        self.assertIn("ValueError", logs)

class TestStreamWrite(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            # заведомо плохой URL, чтобы получить ConnectionError
            return get_currencies(['USD'], url="https://invalid-url-for-test")

        self.wrapped = wrapped

    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)

if __name__ == "__main__":
    unittest.main()
