import sqlite3
from typing import Any, Dict, Iterable, List

from myapp.utils.currencies_api import get_currencies


class DatabaseController:
    """Контроллер доступа к SQLite (:memory:)."""

    def __init__(self) -> None:
        # База данных в памяти, как требует задание.
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Включаем поддержку внешних ключей.
        self.conn.execute("PRAGMA foreign_keys = ON")

        self._create_schema()
        self._seed_data()

    def _create_schema(self) -> None:
        """Создаёт таблицы user, currency и user_currency."""
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );

            CREATE TABLE currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            );

            CREATE TABLE user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            );
            """
        )
        self.conn.commit()

    def _seed_data(self) -> None:
        """Заполняет базу несколькими пользователями и валютами."""
        cur = self.conn.cursor()

        # Пользователи.
        users = [("Михаил",), ("Максим",), ("Алексей",)]
        cur.executemany("INSERT INTO user(name) VALUES (?)", users)

        # Валюты.
        currencies = [
            {
                "num_code": "840",
                "char_code": "USD",
                "name": "Доллар США",
                "value": 90.0,
                "nominal": 1,
            },
            {
                "num_code": "978",
                "char_code": "EUR",
                "name": "Евро",
                "value": 98.0,
                "nominal": 1,
            },
            {
                "num_code": "156",
                "char_code": "CNY",
                "name": "Китайский юань",
                "value": 12.0,
                "nominal": 1,
            },
            {
                "num_code": "826",
                "char_code": "GBP",
                "name": "Фунт стерлингов",
                "value": 110.0,
                "nominal": 1,
            },
        ]
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES (:num_code, :char_code, :name, :value, :nominal)
        """
        cur.executemany(sql, currencies)

        # Связи в таблице user_currency.
        cur.execute("SELECT id, char_code FROM currency")
        code_to_id = {row["char_code"]: row["id"] for row in cur.fetchall()}

        user_currency = [
            (1, code_to_id["USD"]),  # Михаил: USD, EUR.
            (1, code_to_id["EUR"]),
            (2, code_to_id["CNY"]),  # Максим: CNY.
            (3, code_to_id["GBP"]),  # Алексей: GBP.
        ]
        cur.executemany(
            "INSERT INTO user_currency(user_id, currency_id) VALUES (?, ?)",
            user_currency,
        )

        self.conn.commit()

    def currency_create_many(self, data: Iterable[Dict[str, Any]]) -> None:
        """Добавляет несколько валют в таблицу currency."""
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES (:num_code, :char_code, :name, :value, :nominal)
        """
        self.conn.executemany(sql, data)
        self.conn.commit()

    def currency_read_all(self) -> List[sqlite3.Row]:
        """Возвращает список всех валют."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM currency ORDER BY id")
        return cur.fetchall()

    def currency_update_values(self, updates: Dict[str, float]) -> None:
        """Обновляет значение курса (value) по коду валюты.

        Пример словаря updates:
        {"USD": 91.0, "EUR": 100.0}
        """
        cur = self.conn.cursor()
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        for code, value in updates.items():
            cur.execute(sql, (value, code.upper()))
        self.conn.commit()

    def currency_delete(self, currency_id: int) -> None:
        """Удаляет валюту и связанные с ней записи в user_currency."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM user_currency WHERE currency_id = ?", (currency_id,))
        cur.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.conn.commit()
    def sync_currencies_with_cbr(
        self,
        codes: Iterable[str] | None = None,
    ) -> None:
        """Подтягивает свежие курсы валют из API ЦБ.

        """
        currencies = get_currencies(codes)

        cur = self.conn.cursor()
        cur.execute("SELECT id, char_code FROM currency")
        existing = {row["char_code"]: row["id"] for row in cur.fetchall()}

        for c in currencies:
            if c.char_code in existing:
                # Обновляем существующую запись.
                cur.execute(
                    """
                    UPDATE currency
                    SET num_code = ?, name = ?, value = ?, nominal = ?
                    WHERE char_code = ?
                    """,
                    (c.num_code, c.name, c.value, c.nominal, c.char_code),
                )
            else:
                # Создаём новую запись.
                cur.execute(
                    """
                    INSERT INTO currency(num_code, char_code, name, value, nominal)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (c.num_code, c.char_code, c.name, c.value, c.nominal),
                )

        self.conn.commit()

    def users_read_all(self) -> List[sqlite3.Row]:
        """Возвращает всех пользователей."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM user ORDER BY id")
        return cur.fetchall()

    def user_read_one(self, user_id: int) -> sqlite3.Row | None:
        """Возвращает одного пользователя по id или None."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM user WHERE id = ?", (user_id,))
        return cur.fetchone()

    def user_currencies(self, user_id: int) -> List[sqlite3.Row]:
        """Возвращает валюты, на которые подписан пользователь."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT c.*
            FROM currency AS c
            JOIN user_currency AS uc ON uc.currency_id = c.id
            WHERE uc.user_id = ?
            ORDER BY c.id
            """,
            (user_id,),
        )
        return cur.fetchall()
