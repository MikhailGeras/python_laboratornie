class Author:
    """Автор приложения."""

    def __init__(self, name: str, group: str) -> None:
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        """Имя автора."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("name должно быть строкой")
        if not value.strip():
            raise ValueError("name не может быть пустым")
        self._name = value

    @property
    def group(self) -> str:
        """Учебная группа автора."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("group должно быть строкой")
        if not value.strip():
            raise ValueError("group не может быть пустой")
        self._group = value
