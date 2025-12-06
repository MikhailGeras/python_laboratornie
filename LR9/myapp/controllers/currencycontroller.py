from typing import Dict, Iterable, List
from .databasecontroller import DatabaseController

class CurrencyController:

    def __init__(self, db: DatabaseController) -> None:
        """Сохраняет ссылку на объект доступа к БД."""
        self.db = db

    def list_currencies(self) -> List[dict]:
        """Возвращает все валюты в виде списка словарей."""
        rows = self.db.currency_read_all()
        return [dict(row) for row in rows]

    def update_currencies(self, updates: Dict[str, float]) -> None:
        """Обновляет курсы нескольких валют.

        Ожидается словарь вида {"USD": 95.0, "EUR": 100.0}.
        """
        self.db.currency_update_values(updates)

    def delete_currency(self, currency_id: int) -> None:
        """Удаляет валюту по её идентификатору."""
        self.db.currency_delete(currency_id)

    def create_many(self, data: List[dict]) -> None:
        """Создаёт несколько валют сразу."""
        self.db.currency_create_many(data)

    def sync_with_cbr(self, codes: Iterable[str] | None = None) -> None:
        """Обновляет курсы валют по данным API ЦБ."""
        self.db.sync_currencies_with_cbr(codes)
