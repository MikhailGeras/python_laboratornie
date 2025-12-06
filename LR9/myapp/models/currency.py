class Currency:
    """Модель валюты (бизнес-сущность)."""

    def __init__(
        self,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int,
        currency_id: int | None = None,
    ) -> None:
        self.__id = currency_id
        self.__num_code = num_code
        self.char_code = char_code
        self.__name = name
        self.value = value
        self.__nominal = nominal

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, val: int | None) -> None:
        if val is not None and val <= 0:
            raise ValueError("id валюты должен быть положительным")
        self.__id = val

    @property
    def num_code(self) -> str:
        return self.__num_code

    @property
    def char_code(self) -> str:
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str) -> None:
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.__char_code = val.upper()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, val: float) -> None:
        if val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self.__value = float(val)

    @property
    def nominal(self) -> int:
        return self.__nominal
