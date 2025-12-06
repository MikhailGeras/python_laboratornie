class Author:
    """Модель автора лабораторной работы."""

    def __init__(self, name: str, group: str) -> None:
        if not name:
            raise ValueError("Имя автора не может быть пустым")
        if not group:
            raise ValueError("Группа не может быть пустой")
        self.__name = name
        self.__group = group

    @property
    def name(self) -> str:
        return self.__name

    @property
    def group(self) -> str:
        return self.__group
