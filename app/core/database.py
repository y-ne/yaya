import libsql_client
from app.core.config import settings


class Database:
    def __init__(self):
        self._conn = None

    def connect(self):
        if self._conn:
            return self._conn

        if settings.use_embedded_replica:
            self._conn = libsql_client.connect(
                database=settings.local_db_path,
                sync_url=settings.turso_database_url,
                auth_token=settings.turso_auth_token,
                sync_interval=settings.sync_interval
            )
        else:
            self._conn = libsql_client.connect(
                url=settings.turso_database_url,
                auth_token=settings.turso_auth_token
            )

        return self._conn

    def get(self):
        return self._conn if self._conn else self.connect()

    def sync(self):
        if settings.use_embedded_replica and self._conn:
            self._conn.sync()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


db = Database()


def get_db():
    return db.get()
