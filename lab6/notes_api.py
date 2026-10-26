"""REST API заметок на FastAPI (повышенная сложность, №5)."""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, StringConstraints

NoteTitle = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=120,
    ),
]
NoteText = Annotated[
    str,
    StringConstraints(max_length=4000),
]


class NoteCreate(BaseModel):
    """Поля, которые клиент передаёт при создании заметки."""

    title: NoteTitle
    text: NoteText


class Note(NoteCreate):
    """Заметка с идентификатором, выданным сервером."""

    id: int


class NoteStore:
    """Хранилище заметок в памяти процесса."""

    def __init__(self) -> None:
        """Создать пустое хранилище с начальным идентификатором."""
        self._notes: dict[int, Note] = {}
        self._next_id = 1

    def list(self) -> list[Note]:
        """Вернуть заметки в порядке возрастания идентификатора."""
        return [self._notes[key] for key in sorted(self._notes)]

    def get(self, note_id: int) -> Note | None:
        """Найти заметку по идентификатору."""
        return self._notes.get(note_id)

    def create(self, data: NoteCreate) -> Note:
        """Сохранить новую заметку и выдать ей идентификатор."""
        note = Note(id=self._next_id, **data.model_dump())
        self._notes[note.id] = note
        self._next_id += 1
        return note

    def replace(self, note_id: int, data: NoteCreate) -> Note | None:
        """Заменить заметку, если она существует."""
        if note_id not in self._notes:
            return None
        note = Note(id=note_id, **data.model_dump())
        self._notes[note_id] = note
        return note

    def delete(self, note_id: int) -> bool:
        """Удалить заметку и сообщить, была ли она найдена."""
        return self._notes.pop(note_id, None) is not None


def create_app(store: NoteStore | None = None) -> FastAPI:
    """Создать приложение с независимым хранилищем заметок."""
    note_store = NoteStore() if store is None else store
    application = FastAPI(
        title="Lab 6 Notes API",
        version="1.0.0",
        description="REST API заметок в памяти.",
    )

    def missing_note() -> HTTPException:
        """Создать ошибку для отсутствующей заметки."""
        return HTTPException(status_code=404, detail="Note not found")

    @application.get(
        "/notes",
        response_model=list[Note],
        tags=["notes"],
    )
    def list_notes() -> list[Note]:
        """Вернуть все заметки."""
        return note_store.list()

    @application.get(
        "/notes/{note_id}",
        response_model=Note,
        tags=["notes"],
    )
    def get_note(note_id: int) -> Note:
        """Вернуть заметку по идентификатору."""
        note = note_store.get(note_id)
        if note is None:
            raise missing_note()
        return note

    @application.post(
        "/notes",
        response_model=Note,
        status_code=201,
        tags=["notes"],
    )
    def create_note(data: NoteCreate) -> Note:
        """Создать заметку."""
        return note_store.create(data)

    @application.put(
        "/notes/{note_id}",
        response_model=Note,
        tags=["notes"],
    )
    def replace_note(note_id: int, data: NoteCreate) -> Note:
        """Полностью заменить существующую заметку."""
        note = note_store.replace(note_id, data)
        if note is None:
            raise missing_note()
        return note

    @application.delete(
        "/notes/{note_id}",
        status_code=204,
        tags=["notes"],
    )
    def delete_note(note_id: int) -> Response:
        """Удалить заметку."""
        if not note_store.delete(note_id):
            raise missing_note()
        return Response(status_code=204)

    return application


app = create_app()
