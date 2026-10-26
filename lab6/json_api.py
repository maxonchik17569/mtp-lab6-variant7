"""JSON-эндпоинт на FastAPI (средняя сложность, №7)."""

from fastapi import FastAPI
from pydantic import BaseModel

SERVICE_NAME = "lab6-json-api"
VARIANT = 7


class StatusResponse(BaseModel):
    """Схема ответа со статусом сервиса."""

    service: str
    status: str
    variant: int


app = FastAPI(title="Lab 6 JSON API", version="1.0.0")


@app.get("/api/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    """Вернуть состояние сервиса в формате JSON."""
    return StatusResponse(
        service=SERVICE_NAME,
        status="ok",
        variant=VARIANT,
    )
