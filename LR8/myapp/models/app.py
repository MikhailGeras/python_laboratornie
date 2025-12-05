from .author import Author

class App:
    """Простое описание приложения."""

    def __init__(self, name: str, version: str, author: Author) -> None:
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        """Название приложения."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("name должно быть строкой")
        if not value.strip():
            raise ValueError("name не может быть пустым")
        self._name = value

    @property
    def version(self) -> str:
        """Версия приложения."""
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("version должно быть строкой")
        if not value.strip():
            raise ValueError("version не может быть пустой")
        self._version = value

    @property
    def author(self) -> Author:
        """Автор приложения."""
        return self._author

    @author.setter
    def author(self, value: Author) -> None:
        if not isinstance(value, Author):
            raise TypeError("author должен быть экземпляром Author")
        self._author = value
