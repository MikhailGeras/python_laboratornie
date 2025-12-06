from typing import Dict, List, Tuple

from .databasecontroller import DatabaseController


class UserController:
    """Работает с пользователями и их подписками на валюты."""

    def __init__(self, db: DatabaseController) -> None:
        self.db = db

    def list_users(self) -> List[dict]:
        """Возвращает всех пользователей в виде списка словарей."""
        return [dict(row) for row in self.db.users_read_all()]

    def get_user_with_currencies(self, user_id: int) -> Tuple[Dict | None, List[Dict]]:
        """Возвращает пользователя и список его валют.

        Если пользователь не найден, возвращается (None, []).
        """
        user_row = self.db.user_read_one(user_id)
        if user_row is None:
            return None, []
        curr_rows = self.db.user_currencies(user_id)
        return dict(user_row), [dict(r) for r in curr_rows]
