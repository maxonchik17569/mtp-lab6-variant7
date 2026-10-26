"""Тесты страницы книг на Jinja2 (средняя сложность, №9)."""

import unittest

from lab6.template_app import BOOKS, create_app


class TemplateAppTests(unittest.TestCase):
    """Проверки шаблона ``books.html``."""

    def setUp(self) -> None:
        """Создать клиент приложения с книгами по умолчанию."""
        self.client = create_app().test_client()

    def test_index_returns_200(self) -> None:
        """Главная страница отвечает с кодом 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_all_books_are_rendered(self) -> None:
        """Каждая книга из списка попадает в HTML."""
        html = self.client.get("/").get_data(as_text=True)
        self.assertEqual(html.count("<h2>"), len(BOOKS))
        for book in BOOKS:
            self.assertIn(book["title"], html)
            self.assertIn(book["author"], html)

    def test_available_and_borrowed_states(self) -> None:
        """Условие в шаблоне различает доступные и выданные книги."""
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Статус: доступна", html)
        self.assertIn("Статус: выдана", html)

    def test_classic_condition_is_applied(self) -> None:
        """Метка «Классика» появляется только у старых книг."""
        html = self.client.get("/").get_data(as_text=True)
        expected = sum(book["year"] < 1970 for book in BOOKS)
        self.assertEqual(html.count("Классика"), expected)

    def test_last_book_marker_is_single(self) -> None:
        """Метка последней книги выводится ровно один раз."""
        html = self.client.get("/").get_data(as_text=True)
        self.assertEqual(html.count("Последняя книга"), 1)

    def test_custom_collection_is_used(self) -> None:
        """Фабрика передаёт в шаблон именно переданный список."""
        books = [
            {
                "title": "Единственная книга",
                "author": "Тестовый автор",
                "year": 2020,
                "genre": "тест",
                "available": True,
            }
        ]
        client = create_app(books).test_client()
        html = client.get("/").get_data(as_text=True)
        self.assertIn("Единственная книга", html)
        self.assertNotIn("Мастер и Маргарита", html)
        self.assertEqual(html.count("<h2>"), 1)


if __name__ == "__main__":
    unittest.main()
