"""Демонстрация работы без открытия сетевых портов."""

from fastapi.testclient import TestClient

from lab6 import json_api, notes_api, static_app, template_app


def main() -> None:
    """Выполнить запросы через тестовые клиенты и напечатать итог."""
    print("Лабораторная работа №6, вариант 7")
    print("Средняя сложность")

    json_client = TestClient(json_api.app)
    status = json_client.get("/api/status")
    print(f"json_api GET /api/status -> {status.status_code} {status.json()}")

    books_client = template_app.app.test_client()
    books_response = books_client.get("/")
    books_html = books_response.get_data(as_text=True)
    print(
        "template_app GET / -> "
        f"{books_response.status_code}, "
        f"книг в шаблоне: {books_html.count('<h2>')}"
    )
    books_response.close()

    static_client = static_app.app.test_client()
    about_response = static_client.get("/")
    css_response = static_client.get("/static/style.css")
    print(
        "static_app GET / -> "
        f"{about_response.status_code}, "
        f"CSS: {css_response.status_code}"
    )
    print(
        "static_app GET /static/style.css -> "
        f"{css_response.status_code} {css_response.content_type}"
    )
    about_response.close()
    css_response.close()

    print("Повышенная сложность")
    notes_client = TestClient(notes_api.create_app(notes_api.NoteStore()))
    created = notes_client.post(
        "/notes",
        json={"title": "Подготовить отчёт", "text": "Проверить CRUD"},
    )
    print(f"notes_api POST /notes -> {created.status_code} {created.json()}")
    note_id = created.json()["id"]
    listed = notes_client.get("/notes")
    print(f"notes_api GET /notes -> {listed.status_code} {listed.json()}")
    replaced = notes_client.put(
        f"/notes/{note_id}",
        json={"title": "Сдать отчёт", "text": "CRUD проверен"},
    )
    print(
        f"notes_api PUT /notes/{note_id} -> "
        f"{replaced.status_code} {replaced.json()}"
    )
    deleted = notes_client.delete(f"/notes/{note_id}")
    print(f"notes_api DELETE /notes/{note_id} -> {deleted.status_code}")
    missing = notes_client.get(f"/notes/{note_id}")
    print(f"notes_api GET /notes/{note_id} -> {missing.status_code}")

    print(
        "Heroku: Procfile и app.json подготовлены, "
        "живой деплой не выполнялся."
    )
    print("Серверы можно запустить командами из README.md.")


if __name__ == "__main__":
    main()
