from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from myapp.controllers.currencycontroller import CurrencyController
from myapp.controllers.databasecontroller import DatabaseController
from myapp.controllers.usercontroller import UserController
from myapp.models.app import App
from myapp.models.author import Author
from myapp.pages import Pages

AUTHOR = Author(name="Герасимов Михаил", group="P3122")
APP = App(name="CurrenciesListApp", version="2.0.0", author=AUTHOR)

db = DatabaseController()
currency_controller = CurrencyController(db)
user_controller = UserController(db)
pages = Pages(APP, AUTHOR)


class RequestHandler(BaseHTTPRequestHandler):


    def _send_html(self, html: str) -> None:
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _redirect(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _send_static_file(self, path: str) -> None:
        static_root = Path(__file__).parent / "static"
        rel = path[len("/static/") :]
        target = static_root / rel

        if not target.is_file():
            self.send_error(404, "Статический файл не найден")
            return

        if target.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        else:
            content_type = "application/octet-stream"

        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802 (имя метода задано базовым классом)
        """Обрабатывает все GET-запросы."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path.startswith("/static/"):
            self._send_static_file(path)
        elif path == "/":
            self._handle_index()
        elif path == "/author":
            self._handle_author()
        elif path == "/users":
            self._handle_users()
        elif path == "/user":
            self._handle_user(query)
        elif path == "/currencies":
            self._handle_currencies()
        elif path == "/currencies/refresh":
            self._handle_currencies_refresh(query)
        elif path == "/currency/delete":
            self._handle_currency_delete(query)
        elif path == "/currency/update":
            self._handle_currency_update(query)
        else:
            self.send_error(404, "Страница не найдена")

    def _handle_index(self) -> None:
        currencies = currency_controller.list_currencies()
        html = pages.render_index(currencies)
        self._send_html(html)

    def _handle_author(self) -> None:
        html = pages.render_author()
        self._send_html(html)

    def _handle_users(self) -> None:
        users = user_controller.list_users()
        html = pages.render_users(users)
        self._send_html(html)

    def _handle_user(self, query: dict) -> None:
        raw_id = query.get("id", [""])[0]
        try:
            user_id = int(raw_id)
        except ValueError:
            self.send_error(400, "Некорректный id пользователя")
            return

        user, currencies = user_controller.get_user_with_currencies(user_id)
        if user is None:
            self.send_error(404, "Пользователь не найден")
            return

        html = pages.render_user(user, currencies)
        self._send_html(html)

    def _handle_currencies(self) -> None:
        currencies = currency_controller.list_currencies()
        html = pages.render_currencies(currencies)
        self._send_html(html)

    def _handle_currency_delete(self, query: dict) -> None:
        raw_id = query.get("id", [""])[0]
        try:
            currency_id = int(raw_id)
        except ValueError:
            self.send_error(400, "Некорректный id валюты")
            return

        currency_controller.delete_currency(currency_id)
        self._redirect("/currencies")

    def _handle_currency_update(self, query: dict) -> None:
        """Ожидает запрос вида /currency/update?USD=95.5&EUR=100."""
        updates: dict[str, float] = {}
        for code, values in query.items():
            try:
                updates[code.upper()] = float(values[0])
            except (TypeError, ValueError):
                continue

        if updates:
            currency_controller.update_currencies(updates)

        self._redirect("/currencies")

    def _handle_currencies_refresh(self, query: dict) -> None:
        """Обновляет курсы валют по данным API ЦБ.

        Можно передать параметр codes, например:
        /currencies/refresh?codes=USD,EUR
        """
        raw_codes = query.get("codes", [""])[0]
        if raw_codes:
            codes = [c.strip().upper() for c in raw_codes.split(",") if c.strip()]
        else:
            codes = None

        currency_controller.sync_with_cbr(codes)
        self._redirect("/currencies")


def run() -> None:
    """Запускает HTTP-сервер на порту 8080."""
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server started at http://localhost:8080")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run()
