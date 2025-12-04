import sys
import io
import logging
import functools
import requests
import math

def logger(func=None, *, handle=sys.stdout):
    """
    Параметризуемый декоратор логирования.

    """

    def _get_log_functions(handle):
        """
        Вспомогательная функция
        """
        if isinstance(handle, logging.Logger):
            def info(msg: str):
                handle.info(msg)

            def error(msg: str):
                handle.error(msg)
        else:
            def info(msg: str):
                handle.write(f"INFO: {msg}\n")

            def error(msg: str):
                handle.write(f"ERROR: {msg}\n")

        return info, error

    def decorator(real_func):
        @functools.wraps(real_func)  
        def wrapper(*args, **kwargs):
            info, error = _get_log_functions(handle)

            # Логируем начало вызова
            info(f"Calling {real_func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = real_func(*args, **kwargs)
            except Exception as e:
                # Логируем ошибку и пробрасываем её дальше
                error(f"{real_func.__name__} raised {type(e).__name__}: {e}")
                raise
            else:
                # Логируем успешное завершение
                info(f"{real_func.__name__} returned {result!r}")
                return result

        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)


def get_currencies(
    currency_codes: list,
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> dict:
    """
    Получает курсы валют с API Центробанка России.

    :param currency_codes: список кодов валют, например ['USD', 'EUR'].
    :param url: адрес API (по умолчанию официальный CBR JSON).
    :return: словарь вида {"USD": 93.25, "EUR": 101.7}

    """
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        # Любая ошибка сети / URL / тайм-аута
        raise ConnectionError(f"Error while requesting {url}: {e}")

    if response.status_code != 200:
        raise ConnectionError(f"Bad HTTP status {response.status_code} for {url}")

    try:
        data = response.json()
    except ValueError as e:
        # Невалидный JSON
        raise ValueError(f"Invalid JSON from API: {e}")

    if "Valute" not in data:
        raise KeyError("Key 'Valute' not found in JSON")

    valute = data["Valute"]

    # 5. Собираем словарь курсов для нужных кодов
    result = {}
    for code in currency_codes:
        # 5.1. Проверяем, есть ли такая валюта
        if code not in valute:
            raise KeyError(f"Currency code {code!r} not found in API data")

        currency_info = valute[code]

        # 5.2. Берём курс из поля "Value"
        if "Value" not in currency_info:
            raise KeyError(f"'Value' key is missing for currency {code!r}")

        rate = currency_info["Value"]

        # 5.3. Проверяем тип курса
        if not isinstance(rate, (int, float)):
            raise TypeError(
                f"Rate for currency {code!r} has wrong type: {type(rate)}"
            )

        result[code] = rate

    return result


logged_get_currencies = logger(handle=sys.stdout)(get_currencies)

file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("currency.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)

# Функция, которая логирует все вызовы в файл
file_logged_get_currencies = logger(handle=file_logger)(get_currencies)



quad_logger = logging.getLogger("quadratic")
quad_logger.setLevel(logging.INFO)

quad_handler = logging.StreamHandler(sys.stdout)
quad_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
quad_logger.addHandler(quad_handler)


@logger(handle=quad_logger)
def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение ax^2 + bx + c = 0.
    Возвращает кортеж корней (0, 1 или 2 корня).

    """

    for name, value in (("a", a), ("b", b), ("c", c)):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Coefficient {name} has invalid type: {type(value)}")

    if a == 0 and b == 0:
        quad_logger.critical("Both a and b are zero — not a valid equation")
        raise ValueError("Both a and b are zero")

    if a == 0:
        x = -c / b
        return (x,)

    D = b ** 2 - 4 * a * c

    if D < 0:
        quad_logger.warning(f"Discriminant < 0 (D={D}), no real roots")
        return tuple()

    if D == 0:
        x = -b / (2 * a)
        return (x,)

    sqrt_D = math.sqrt(D)
    x1 = (-b + sqrt_D) / (2 * a)
    x2 = (-b - sqrt_D) / (2 * a)
    return (x1, x2)


if __name__ == "__main__":
    print("=== Пример logged_get_currencies (stdout) ===")
    try:
        rates = logged_get_currencies(["USD", "EUR"])
        print("Курсы валют:", rates)
    except Exception as e:
        print("Ошибка при получении валют:", e)

    print("\n=== Пример file_logged_get_currencies (лог пишется в currency.log) ===")
    try:
        rates = file_logged_get_currencies(["USD"])
        print("Курс USD:", rates)
    except Exception as e:
        print("Ошибка при получении валют (file):", e)
    try:
        rates = file_logged_get_currencies(["EUR"])
        print("Курс EUR:", rates)
    except Exception as e:
        print("Ошибка при получении валют (file):", e)

    print("\n=== Примеры solve_quadratic ===")
    print("Два корня:", solve_quadratic(1, -3, 2))
    print("Нет вещественных корней:", solve_quadratic(1, 0, 1))
    try:
        solve_quadratic("abc", 1, 1)
    except Exception as e:
        print("Ошибка (ожидаем TypeError):", e)
    try:
        solve_quadratic(0, 0, 1)
    except Exception as e:
        print("Ошибка (ожидаем CRITICAL + ValueError):", e)
