# ЛР7 — «Декоратор-логгер и работа с внешним API (курсы валют ЦБ РФ)»

**Автор:** Герасимов Михаил, группа P3122  
**Среда:** Python 3.13, `requests`, `logging`, `unittest`

## Навигация

- Основной код: [main.py](./main.py)  
- Тесты: [test.py](./test.py)  
- Файл с логами курсов: `currency.log` (создаётся при запуске `main.py`)

---

## Постановка задачи

1. Реализовать **параметризуемый декоратор `logger`**, который:
   - умеет логировать в:
     - стандартный поток (`sys.stdout`),
     - любой «потокоподобный» объект (`io.StringIO`),
     - объект `logging.Logger` (в т.ч. лог в файл);
   - при каждом вызове функции:
     - логирует начало вызова (имя функции и аргументы),
     - логирует успешное завершение (возвращаемое значение),
     - при исключении логирует его тип и текст и **пробрасывает исключение дальше**;
   - не меняет сигнатуру оборачиваемой функции (используется `functools.wraps`).

2. Реализовать **функцию `get_currencies(currency_codes, url)`**, которая:
   - делает HTTP-запрос к API ЦБ РФ;
   - из ответа JSON извлекает курсы валют;
   - возвращает словарь вида `{"USD": 93.25, "EUR": 101.7}`;
   - выбрасывает осмысленные исключения при ошибках (без логирования внутри).

3. Обернуть `get_currencies` в декоратор `logger` с разными вариантами `handle`:
   - логирование в `sys.stdout`;
   - логирование в файл через `logging`.

4. Реализовать демонстрационную функцию `solve_quadratic(a, b, c)` с разными уровнями логирования:
   - INFO, WARNING, ERROR, CRITICAL.

5. Написать **модульные тесты**:
   - для `get_currencies` (поведение и исключения);
   - для декоратора (логирование в `io.StringIO` и проброс ошибок).

---

## Реализация

### 1. Декоратор `logger`

Файл: `main.py`.

Сигнатура:

```python
def logger(func=None, *, handle=sys.stdout):
```

**Идея:**

- Декоратор можно использовать:
  - как `@logger` — лог в `sys.stdout` по умолчанию;
  - как `@logger(handle=stream)` — лог в любой объект с `.write()` (например, `io.StringIO`);
  - как `@logger(handle=log)` — лог через `logging.Logger`.

Внутри декоратора:

1. Вспомогательная функция `_get_log_functions(handle)` определяет способ логирования.
2. Обёртка `wrapper(*args, **kwargs)` логирует старт, завершение и ошибки.
3. Используется `functools.wraps`, чтобы сохранить метаданные функции.

---

### 2. Функция `get_currencies` 

Файл: `main.py`.

```python
def get_currencies(
    currency_codes: list,
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> dict:
```

**Основная логика:**

1. Делает HTTP-запрос к API ЦБ РФ (`requests.get(url, timeout=5)`).
2. Проверяет статус-код и структуру JSON.
3. Проверяет наличие нужных валют и корректность типов.
4. Возвращает словарь вида `{"USD": <курс>, "EUR": <курс>}`.
5. При ошибках выбрасывает исключения (`ConnectionError`, `ValueError`, `KeyError`, `TypeError`).

---

### 3. Логирование в разные потоки

#### 3.1. В `sys.stdout`
```python
logged_get_currencies = logger(handle=sys.stdout)(get_currencies)
```

#### 3.2. В файл через `logging.Logger`
```python
file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("currency.log", encoding="utf-8")
file_logger.addHandler(file_handler)
file_logged_get_currencies = logger(handle=file_logger)(get_currencies)
```

---

## Тестирование

Файл: `test.py`.

- Проверяется корректность работы `get_currencies`.
- Проверяется проброс и логирование исключений.
- Тестируется поведение декоратора через `io.StringIO`.
- Проверяется, что при ошибках в логах появляется `ERROR` и тип исключения.

