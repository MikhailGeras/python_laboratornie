class User:
    """Модель пользователя."""

    def __init__(self, user_id: int, name: str) -> None:
        if user_id <= 0:
            raise ValueError("id пользователя должен быть положительным")
        if not name:
            raise ValueError("Имя пользователя не может быть пустым")
        self.__id = user_id
        self.__name = name

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name
