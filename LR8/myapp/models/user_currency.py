class UserCurrency:
    """Связь пользователь–валюта"""

    def __init__(self, record_id: int, user_id: int, currency_id: str) -> None:
        self.id = record_id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        """Идентификатор записи."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id должен быть целым числом")
        if value <= 0:
            raise ValueError("id должен быть положительным")
        self._id = value

    @property
    def user_id(self) -> int:
        """ID пользователя."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("user_id должен быть целым числом")
        if value <= 0:
            raise ValueError("user_id должен быть положительным")
        self._user_id = value

    @property
    def currency_id(self) -> str:
        """ID валюты."""
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("currency_id должно быть строкой")
        if not value.strip():
            raise ValueError("currency_id не может быть пустым")
        self._currency_id = value
