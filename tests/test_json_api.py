"""Тесты JSON-эндпоинта FastAPI (средняя сложность, №7)."""

import unittest

from fastapi.testclient import TestClient

from lab6.json_api import app


class JsonApiTests(unittest.TestCase):
    """Проверки маршрута ``/api/status``."""

    def setUp(self) -> None:
        """Создать тестовый клиент без сетевого порта."""
        self.client = TestClient(app)

    def test_status_returns_200(self) -> None:
        """Маршрут статуса отвечает с кодом 200."""
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)

    def test_status_payload_is_json(self) -> None:
        """Ответ содержит ожидаемые поля и тип JSON."""
        response = self.client.get("/api/status")
        self.assertEqual(
            response.headers["content-type"],
            "application/json",
        )
        self.assertEqual(
            response.json(),
            {
                "service": "lab6-json-api",
                "status": "ok",
                "variant": 7,
            },
        )

    def test_variant_is_seven(self) -> None:
        """В ответе указан вариант лабораторной работы."""
        response = self.client.get("/api/status")
        self.assertEqual(response.json()["variant"], 7)


if __name__ == "__main__":
    unittest.main()
