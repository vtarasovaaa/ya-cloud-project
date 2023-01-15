import uuid
from typing import List

import ydb

from pydantic import BaseSettings, BaseModel


class NoteStorageSettings(BaseSettings):
    endpoint: str
    database: str
    driver_timeout: int = 10

    class Config:
        env_prefix = "NOTE_STORAGE_"


class Note(BaseModel):
    id: str
    author: str
    text: str


class NoteStorage:
    def __init__(self, settings: NoteStorageSettings):
        self._settings = settings
        self._driver = ydb.Driver(endpoint=settings.endpoint, database=settings.database)

    def _get_config(self):
        endpoint = self._settings.endpoint
        database = self._settings.database
        if endpoint is None or database is None:
            raise AssertionError("Нужно указать обе переменные окружения")
        credentials = ydb.construct_credentials_from_environ()
        return ydb.DriverConfig(endpoint, database, credentials=credentials)

    def _execute(self, query, params):
        with ydb.Driver(self._get_config()) as driver:
            try:
                driver.wait(timeout=self._settings.driver_timeout)
            except TimeoutError:
                print("Connect failed to YDB")
                print("Last reported errors by discovery:")
                print(driver.discovery_debug_details())
                return None

            session = driver.table_client.session().create()
            prepared_query = session.prepare(query)

            return session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query,
                params,
                commit_tx=True
            )

    def insert_note(self, author: str, text: str) -> None:
        query = """
            DECLARE $id AS Utf8;
            DECLARE $author AS Utf8;
            DECLARE $text AS Utf8;

            UPSERT INTO notes (id, author, text) VALUES ($id, $author, $text);
            """
        params = {'$id': str(uuid.uuid4()), '$author': author, '$text': text}
        self._execute(query, params)

    def get_notes(self) -> List[Note]:
        query = 'SELECT id, author, text FROM notes;'
        query_result = self._execute(query, {})

        if not query_result:
            return []

        return [
            Note(id=row.id.decode(), author=row.author.decode(), text=row.text.decode()) for row in query_result[0].rows
        ]
