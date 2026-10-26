"""Статическая страница на Flask (средняя сложность, №3)."""

from flask import Flask, render_template


def create_app() -> Flask:
    """Создать Flask-приложение со статической страницей."""
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        """Показать страницу о лабораторной работе."""
        return render_template("about.html")

    return app


app = create_app()
