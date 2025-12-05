from typing import List
import xml.etree.ElementTree as ET

import requests

from myapp.models import Currency

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


def get_currencies() -> List[Currency]:
    """
    Получает список валют с сайта ЦБ РФ.

    Возвращает:
        Список объектов Currency.

    Выбрасывает:
        RuntimeError: при ошибке сети, разборе XML или пустом ответе.
    """
    try:
        response = requests.get(CBR_URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError("Ошибка при запросе к ЦБ РФ") from exc

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as exc:
        raise RuntimeError("Ошибка разбора XML ЦБ РФ") from exc

    currencies: List[Currency] = []

    for valute in root.findall("Valute"):
        currency_id = (valute.get("ID") or "").strip()
        num_code_text = valute.findtext("NumCode", default="0")
        char_code = (valute.findtext("CharCode", default="") or "").strip()
        name = (valute.findtext("Name", default="") or "").strip()
        nominal_text = valute.findtext("Nominal", default="1")
        value_text = (valute.findtext("Value", default="0") or "").replace(",", ".")

        try:
            num_code = int(num_code_text)
            nominal = int(nominal_text)
            value = float(value_text)
        except ValueError:
            continue

        if not currency_id or not char_code or not name:
            continue

        currencies.append(
            Currency(
                currency_id=currency_id,
                num_code=num_code,
                char_code=char_code,
                name=name,
                value=value,
                nominal=nominal,
            )
        )

    if not currencies:
        raise RuntimeError("Список валют пуст")

    return currencies
