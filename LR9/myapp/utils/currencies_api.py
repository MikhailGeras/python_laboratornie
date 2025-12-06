from typing import Iterable, List, Dict
from datetime import date, timedelta
import requests
from myapp.models.currency import Currency


CBR_DAILY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_currencies(
    currency_codes: Iterable[str] | None = None,
    url: str = CBR_DAILY_URL,
) -> List[Currency]:
    """Получить список валют с актуальными курсами.

    """

    # --- 1. HTTP-запрос (как в ЛР7) ---
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as exc:
        # Любая ошибка сети / URL / тайм-аута
        raise ConnectionError(f"Error while requesting {url}: {exc}") from exc

    if response.status_code != 200:
        raise ConnectionError(f"Bad HTTP status {response.status_code} for {url}")

    # --- 2. Разбор JSON ---
    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError(f"Invalid JSON from API: {exc}") from exc

    if "Valute" not in data:
        raise KeyError("Key 'Valute' not found in JSON")

    valute_dict = data["Valute"]
    if not isinstance(valute_dict, dict):
        raise TypeError("Field 'Valute' must be a dict in JSON")

    # --- 3. Подготовка множества кодов валют (если задано) ---
    codes_filter = (
        {code.upper() for code in currency_codes}
        if currency_codes
        else None
    )

    # --- 4. Формирование списка моделей Currency ---
    currencies: List[Currency] = []
    next_id = 1

    for val in valute_dict.values():
        # Структура daily_json: ID, NumCode, CharCode, Nominal, Name, Value, Previous, ...
        char_code = val.get("CharCode")
        if not isinstance(char_code, str):
            # пропускаем странные записи
            continue

        char_code = char_code.upper()
        if codes_filter is not None and char_code not in codes_filter:
            continue

        num_code_raw = val.get("NumCode")
        nominal_raw = val.get("Nominal")
        name = val.get("Name", "")
        value_raw = val.get("Value")

        # Проверяем наличие обязательных полей (логика близка к ЛР7)
        if num_code_raw is None:
            raise KeyError(f"'NumCode' key is missing for currency {char_code!r}")
        if value_raw is None:
            raise KeyError(f"'Value' key is missing for currency {char_code!r}")
        if nominal_raw is None:
            raise KeyError(f"'Nominal' key is missing for currency {char_code!r}")

        try:
            num_code = int(num_code_raw)
            nominal = int(nominal_raw)
            value = float(value_raw)
        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"Wrong types for currency {char_code!r}: "
                f"NumCode={type(num_code_raw)}, "
                f"Nominal={type(nominal_raw)}, "
                f"Value={type(value_raw)}"
            ) from exc

        currency = Currency(
            currency_id=next_id,
            num_code=num_code,
            char_code=char_code,
            name=name,
            value=value,
            nominal=nominal,
        )
        currencies.append(currency)
        next_id += 1

    if not currencies:
        raise ValueError("No currencies found for given codes.")

    return currencies


from datetime import date, timedelta
from typing import Iterable
import requests  # если уже импортирован выше – второй раз не надо


def get_history_for_codes(
    codes: Iterable[str],
    months: int = 3,
    points: int = 8,
) -> dict[str, list[dict[str, float | str]]]:
    """Получить реальную историю курсов для набора валют.

    Используем архив ЦБ РФ, но делаем МАЛО запросов:
    - берём примерно `points` дат за последние `months` месяцев,
    - на КАЖДУЮ дату — только ОДИН запрос,
    - из ответа забираем сразу все нужные валюты.

    Возвращает:
        {
          "USD": [{"date": "YYYY-MM-DD", "value": 90.12}, ...],
          "EUR": [...],
        }
    """
    codes_upper = sorted({c.upper() for c in codes})
    history: dict[str, list[dict[str, float | str]]] = {code: [] for code in codes_upper}

    if not codes_upper:
        return history

    end_date = date.today()
    total_days = months * 30
    start_date = end_date - timedelta(days=total_days)

    # Гарантируем хотя бы 2 точки
    if points < 2:
        points = 2

    # Шаг по времени так, чтобы всего было ≈ points дат
    step = total_days // (points - 1) or 1

    # Строим список дат (равномерно от start_date до end_date)
    date_list: list[date] = []
    current = start_date
    while current < end_date and len(date_list) < points - 1:
        date_list.append(current)
        current = current + timedelta(days=step)
    date_list.append(end_date)  # последняя точка — сегодня

    for d in date_list:
        url = (
            f"https://www.cbr-xml-daily.ru/archive/"
            f"{d.year}/{d.month:02d}/{d.day:02d}/daily_json.js"
        )

        try:
            resp = requests.get(url, timeout=2)
        except requests.RequestException:
            # Если конкретный день не доступен — просто пропускаем
            continue

        if resp.status_code != 200:
            continue

        try:
            data = resp.json()
        except ValueError:
            continue

        valute = data.get("Valute")
        if not isinstance(valute, dict):
            continue

        for code in codes_upper:
            val = valute.get(code)
            if not isinstance(val, dict):
                continue

            value_raw = val.get("Value")
            if value_raw is None:
                continue

            try:
                value = float(value_raw)
            except (TypeError, ValueError):
                continue

            history[code].append(
                {
                    "date": d.isoformat(),
                    "value": round(value, 4),
                }
            )

    return history
