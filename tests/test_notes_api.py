"""Тесты REST API заметок (повышенная сложность, №5)."""

import unittest

from fastapi.testclient import TestClient

from lab6.notes_api import NoteStore, create_app


class NotesApiTests(unittest.TestCase):
    """Проверки CRUD-маршрутов ``/notes``."""

    def setUp(self) -> None:
        """Создать приложение с отдельным хранилищем для теста."""
        self.client = TestClient(create_app(NoteStore()))

    def create_note(
        self,
        title: str = "Заметка",
        text: str = "Текст заметки",
    ) -> dict[str, object]:
        """Создать заметку через API и вернуть её тело."""
        response = self.client.post(
            "/notes",
            json={"title": title, "text": text},
        )
        self.assertEqual(response.status_code, 201)
        return response.json()

    def test_list_is_empty_initially(self) -> None:
        """Новое хранилище отдаёт пустой список."""
        response = self.client.get("/notes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_returns_201_and_stores_note(self) -> None:
        """POST создаёт заметку с id и сохраняет её."""
        body = self.create_note("План", "Проверить CRUD")
        self.assertEqual(body["id"], 1)
        self.assertEqual(body["title"], "План")
        self.assertEqual(body["text"], "Проверить CRUD")
        listed = self.client.get("/notes").json()
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0], body)

    def test_create_strips_title_whitespace(self) -> None:
        """Заголовок нормализуется удалением пробелов по краям."""
        body = self.create_note("  План  ")
        self.assertEqual(body["title"], "План")

    def test_blank_title_returns_422(self) -> None:
        """Пустой заголовок отклоняется валидацией Pydantic."""
        response = self.client.post(
            "/notes",
            json={"title": "   ", "text": "текст"},
        )
        self.assertEqual(response.status_code, 422)

    def test_missing_text_returns_422(self) -> None:
        """Поле ``text`` обязательно для создания заметки."""
        response = self.client.post("/notes", json={"title": "План"})
        self.assertEqual(response.status_code, 422)

    def test_get_returns_created_note(self) -> None:
        """GET по id возвращает созданную заметку."""
        note_id = int(self.create_note()["id"])
        response = self.client.get(f"/notes/{note_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], note_id)

    def test_get_missing_note_returns_404(self) -> None:
        """Неизвестный id приводит к ответу 404."""
        response = self.client.get("/notes/999")
        self.assertEqual(response.status_code, 404)

    def test_put_replaces_note(self) -> None:
        """PUT заменяет поля, сохраняя идентификатор."""
        note_id = int(self.create_note("Старое", "Старый текст")["id"])
        response = self.client.put(
            f"/notes/{note_id}",
            json={"title": "Новое", "text": "Новый текст"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": note_id, "title": "Новое", "text": "Новый текст"},
        )
        stored = self.client.get(f"/notes/{note_id}").json()
        self.assertEqual(stored, response.json())

    def test_put_missing_note_returns_404(self) -> None:
        """PUT для неизвестного id приводит к ответу 404."""
        response = self.client.put(
            "/notes/999",
            json={"title": "Новое", "text": "Текст"},
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_returns_204_then_404(self) -> None:
        """DELETE удаляет заметку, повторный вызов даёт 404."""
        note_id = int(self.create_note()["id"])
        deleted = self.client.delete(f"/notes/{note_id}")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(deleted.content, b"")
        self.assertEqual(self.client.get(f"/notes/{note_id}").status_code, 404)
        again = self.client.delete(f"/notes/{note_id}")
        self.assertEqual(again.status_code, 404)

    def test_stores_are_isolated_between_apps(self) -> None:
        """Два приложения с разными хранилищами не делят данные."""
        other = TestClient(create_app(NoteStore()))
        self.create_note("Только в первом")
        self.assertEqual(other.get("/notes").json(), [])


if __name__ == "__main__":
    unittest.main()
