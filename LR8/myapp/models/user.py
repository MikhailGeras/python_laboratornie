class User:
    """Пользователь приложения."""

    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    @property
    def id(self) -> int:
        """Идентификатор пользователя."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id должен быть целым числом")
        if value <= 0:
            raise ValueError("id должен быть положительным")
        self._id = value

    @property
    def name(self) -> str:
        """Имя пользователя."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("name должно быть строкой")
        if not value.strip():
            raise ValueError("name не может быть пустым")
        self._name = value
