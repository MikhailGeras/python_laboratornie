from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import date, timedelta
from typing import List, Dict, Any
import random

from jinja2 import Environment, PackageLoader, select_autoescape

from myapp.models import Author, App, User, UserCurrency
from myapp.utils.currencies_api import get_currencies

# Инициализация Jinja2
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

tmpl_index = env.get_template("index.html")
tmpl_users = env.get_template("users.html")
tmpl_user = env.get_template("user.html")
tmpl_currencies = env.get_template("currencies.html")
tmpl_author = env.get_template("author.html")

# Автор и приложение
main_author = Author("Герасимов Михаил", "P3122")
main_app = App("CurrenciesApp", "1.0", main_author)

# Пользователи
users: List[User] = [
    User(user_id=1, name="Максим"),
    User(user_id=2, name="Миша"),
    User(user_id=3, name="Алексей"),
]

# Подписки пользователей на валюты (ID из XML ЦБ)
subscriptions: List[UserCurrency] = [
    UserCurrency(record_id=1, user_id=1, currency_id="R01235"),  # USD
    UserCurrency(record_id=2, user_id=1, currency_id="R01239"),  # EUR
    UserCurrency(record_id=3, user_id=2, currency_id="R01235"),  # USD
    UserCurrency(record_id=4, user_id=3, currency_id="R01010"),  # ещё валюта
]


def build_fake_history(value: float) -> Dict[str, List[Any]]:
    """
    Строит условную историю курса за 3 месяца.

    История нужна для графиков и основана на текущем значении
    с небольшими случайными отклонениями.
    """
    labels: List[str] = []
    values: List[float] = []

    start = date.today() - timedelta(days=90)
    current_date = start
    current_value = value

    while current_date <= date.today():
        labels.append(current_date.strftime("%d.%m"))
        current_value += random.uniform(-0.3, 0.3)
        values.append(round(current_value, 2))
        current_date += timedelta(days=7)

    return {"labels": labels, "values": values}


class SimpleHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов."""

    def _render(self, html: str) -> None:
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            self.handle_index()
        elif path == "/users":
            self.handle_users()
        elif path == "/user":
            self.handle_user(query)
        elif path == "/currencies":
            self.handle_currencies()
        elif path == "/author":
            self.handle_author()
        elif path.startswith("/static/"):
            self.handle_static(path)
        else:
            self.send_error(404, "Страница не найдена")

    def handle_index(self) -> None:
        html = tmpl_index.render(
            title="Главная",
            app_name=main_app.name,
            app_version=main_app.version,
            author_name=main_author.name,
            group=main_author.group,
        )
        self._render(html)

    def handle_users(self) -> None:
        html = tmpl_users.render(
            title="Пользователи",
            users=users,
            app_name=main_app.name,
            app_version=main_app.version,
            author_name=main_author.name,
            group=main_author.group,
        )
        self._render(html)

    def handle_user(self, query: Dict[str, List[str]]) -> None:
        user_param = query.get("id", [""])[0]
        try:
            user_id = int(user_param)
        except ValueError:
            self.send_error(400, "Некорректный параметр id")
            return

        user = next((u for u in users if u.id == user_id), None)
        if user is None:
            self.send_error(404, "Пользователь не найден")
            return

        error = ""
        try:
            currencies = get_currencies()
        except RuntimeError as exc:
            currencies = []
            error = str(exc)

        subscribed_ids = {
            s.currency_id for s in subscriptions if s.user_id == user_id
        }
        user_currencies = [c for c in currencies if c.id in subscribed_ids]

        charts: List[Dict[str, List[Any]]] = []
        for c in user_currencies:
            history = build_fake_history(c.value)
            charts.append(
                {
                    "char": c.char_code,
                    "labels": history["labels"],
                    "values": history["values"],
                }
            )

        html = tmpl_user.render(
            title=user.name,
            user=user,
            currencies=user_currencies,
            charts=charts,
            error=error,
            app_name=main_app.name,
            app_version=main_app.version,
            author_name=main_author.name,
            group=main_author.group,
        )
        self._render(html)

    def handle_currencies(self) -> None:
        error = ""
        try:
            currencies = get_currencies()
        except RuntimeError as exc:
            currencies = []
            error = str(exc)

        html = tmpl_currencies.render(
            title="Курсы валют",
            currencies=currencies,
            error=error,
            app_name=main_app.name,
            app_version=main_app.version,
            author_name=main_author.name,
            group=main_author.group,
        )
        self._render(html)

    def handle_author(self) -> None:
        html = tmpl_author.render(
            title="Автор",
            app_name=main_app.name,
            app_version=main_app.version,
            author_name=main_author.name,
            group=main_author.group,
        )
        self._render(html)

    def handle_static(self, path: str) -> None:
        if path == "/static/style.css":
            try:
                with open("myapp/static/style.css", "rb") as css:
                    data = css.read()
            except FileNotFoundError:
                self.send_error(404, "style.css не найден")
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404, "Статический файл не найден")


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Запускает HTTP-сервер."""
    httpd = HTTPServer((host, port), SimpleHandler)
    print(f"Сервер запущен на http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
