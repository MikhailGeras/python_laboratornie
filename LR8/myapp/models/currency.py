class Currency:
    """Валюта из ЦБ РФ."""

    def __init__(
        self,
        currency_id: str,
        num_code: int,
        char_code: str,
        name: str,
        value: float,
        nominal: int,
    ) -> None:
        self.id = currency_id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> str:
        """Строковый идентификатор валюты."""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("id должно быть строкой")
        if not value.strip():
            raise ValueError("id не может быть пустым")
        self._id = value

    @property
    def num_code(self) -> int:
        """Цифровой код валюты."""
        return self._num_code

    @num_code.setter
    def num_code(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("num_code должен быть целым числом")
        if value <= 0:
            raise ValueError("num_code должен быть положительным")
        self._num_code = value

    @property
    def char_code(self) -> str:
        """Буквенный код валюты."""
        return self._char_code

    @char_code.setter
    def char_code(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("char_code должен быть строкой")
        if not value.strip():
            raise ValueError("char_code не может быть пустым")
        self._char_code = value

    @property
    def name(self) -> str:
        """Название валюты."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("name должно быть строкой")
        if not value.strip():
            raise ValueError("name не может быть пустым")
        self._name = value

    @property
    def value(self) -> float:
        """Текущий курс валюты."""
        return self._value

    @value.setter
    def value(self, amount: float) -> None:
        if not isinstance(amount, (int, float)):
            raise TypeError("value должно быть числом")
        if amount <= 0:
            raise ValueError("value должно быть положительным")
        self._value = float(amount)

    @property
    def nominal(self) -> int:
        """Номинал валюты."""
        return self._nominal

    @nominal.setter
    def nominal(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("nominal должен быть целым числом")
        if value <= 0:
            raise ValueError("nominal должен быть положительным")
        self._nominal = value
