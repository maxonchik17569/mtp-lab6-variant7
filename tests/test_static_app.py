"""Тесты статической страницы Flask (средняя сложность, №3)."""

import unittest

from lab6.static_app import app


class StaticAppTests(unittest.TestCase):
    """Проверки страницы ``about.html`` и файла ``style.css``."""

    def setUp(self) -> None:
        """Создать тестовый клиент Flask."""
        self.client = app.test_client()

    def test_index_returns_200(self) -> None:
        """Статическая страница отвечает с кодом 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_page_content(self) -> None:
        """Страница содержит заголовок и сведения о варианте."""
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Статическая страница", html)
        self.assertIn("Вариант", html)
        self.assertIn("7", html)

    def test_stylesheet_is_linked(self) -> None:
        """В HTML подключён файл ``static/style.css``."""
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('rel="stylesheet"', html)
        self.assertIn('href="/static/style.css"', html)

    def test_css_is_served(self) -> None:
        """Flask отдаёт CSS с корректным MIME-типом."""
        response = self.client.get("/static/style.css")
        self.addCleanup(response.close)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.headers["content-type"])

    def test_css_sets_colors_and_spacing(self) -> None:
        """CSS задаёт цвета, отступы и оформление карточки."""
        response = self.client.get("/static/style.css")
        self.addCleanup(response.close)
        css = response.get_data(as_text=True)
        self.assertIn("--accent", css)
        self.assertIn(".card", css)
        self.assertIn("padding", css)
        self.assertIn("background", css)
        self.assertIn("margin", css)


if __name__ == "__main__":
    unittest.main()
