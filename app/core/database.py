import libsql
from app.core.config import settings


class Database:
    def __init__(self):
        self._conn = None

    def connect(self):
        if self._conn:
            return self._conn

        self._conn = libsql.connect(
            database=settings.turso_database_url,
            auth_token=settings.turso_auth_token
        )

        return self._conn

    def get(self):
        return self._conn if self._conn else self.connect()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


db = Database()


def get_db():
    return db.get()
