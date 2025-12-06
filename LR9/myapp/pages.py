# myapp/pages.py
from __future__ import annotations

from jinja2 import Environment, PackageLoader, select_autoescape

from myapp.models.author import Author
from myapp.models.app import App


class Pages:
    """Отвечает за рендеринг HTML-страниц через Jinja2."""

    def __init__(self, app: App, author: Author) -> None:
        self.app = app
        self.author = author

        self.env = Environment(
            loader=PackageLoader("myapp"),
            autoescape=select_autoescape(),
        )

        self.index_tmpl = self.env.get_template("index.html")
        self.currencies_tmpl = self.env.get_template("currencies.html")
        self.users_tmpl = self.env.get_template("users.html")
        self.user_tmpl = self.env.get_template("user.html")
        self.author_tmpl = self.env.get_template("author.html")

    def render_index(self, currencies: list[dict]) -> str:
        return self.index_tmpl.render(
            app=self.app,
            author=self.author,
            currencies=currencies,
        )

    def render_currencies(self, currencies: list[dict]) -> str:
        return self.currencies_tmpl.render(
            app=self.app,
            author=self.author,
            currencies=currencies,
        )

    def render_users(self, users: list[dict]) -> str:
        return self.users_tmpl.render(
            app=self.app,
            author=self.author,
            users=users,
        )

    def render_user(self, user: dict, currencies: list[dict]) -> str:
        return self.user_tmpl.render(
            app=self.app,
            author=self.author,
            user=user,
            currencies=currencies,
        )

    def render_author(self) -> str:
        return self.author_tmpl.render(
            app=self.app,
            author=self.author,
        )
