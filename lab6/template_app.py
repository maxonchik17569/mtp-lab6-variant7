"""Страница книг на Flask и Jinja2 (средняя сложность, №9)."""

from typing import TypedDict

from flask import Flask, render_template


class Book(TypedDict):
    """Описание книги для шаблона."""

    title: str
    author: str
    year: int
    genre: str
    available: bool


BOOKS: tuple[Book, ...] = (
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "year": 1967,
        "genre": "роман",
        "available": True,
    },
    {
        "title": "Пикник на обочине",
        "author": "Аркадий и Борис Стругацкие",
        "year": 1972,
        "genre": "фантастика",
        "available": False,
    },
    {
        "title": "Солярис",
        "author": "Станислав Лем",
        "year": 1961,
        "genre": "фантастика",
        "available": True,
    },
    {
        "title": "Дюна",
        "author": "Фрэнк Герберт",
        "year": 1965,
        "genre": "фантастика",
        "available": False,
    },
)


def create_app(books: list[Book] | None = None) -> Flask:
    """Создать Flask-приложение с каталогом книг."""
    app = Flask(__name__)
    selected_books = list(BOOKS) if books is None else list(books)

    @app.get("/")
    def index() -> str:
        """Показать страницу с книгами."""
        return render_template("books.html", books=selected_books)

    return app


app = create_app()
