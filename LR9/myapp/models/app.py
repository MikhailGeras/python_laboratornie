from .author import Author

class App:
    """Модель приложения (метаданные)."""

    def __init__(self, name: str, version: str, author: Author) -> None:
        if not name:
            raise ValueError("Название приложения не может быть пустым")
        self.__name = name
        self.__version = version
        self.__author = author

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    @property
    def author(self) -> Author:
        return self.__author
