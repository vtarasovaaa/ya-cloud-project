from functools import cache
from typing import Optional

import fastapi
from pydantic import BaseModel

from storage.note_storage import Note, NoteStorage, NoteStorageSettings


class NoteRequest(BaseModel):
    author: Optional[str]
    text: str


class NotesResponse(BaseModel):
    notes: list[Note]

@cache
def get_note_storage() -> NoteStorage:
    return NoteStorage(NoteStorageSettings())


def get_notes(storage: NoteStorage = fastapi.Depends(get_note_storage)) -> NotesResponse:
    return NotesResponse(notes=storage.get_notes())


def save_note(data: NoteRequest, storage: NoteStorage = fastapi.Depends(get_note_storage)) -> None:
    return storage.insert_note(**data.dict())
