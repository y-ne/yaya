class SkelModel:
    TABLE_NAME = "skels"

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS skels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skel_text TEXT NOT NULL,
            skel_char VARCHAR(255),
            skel_int INTEGER,
            skel_float REAL,
            skel_bool INTEGER DEFAULT 0,
            skel_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    INSERT = """
        INSERT INTO skels (skel_text, skel_char, skel_int, skel_float, skel_bool, skel_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    SELECT_ALL = """
        SELECT id, skel_text, skel_char, skel_int, skel_float, skel_bool, skel_json, created_at, updated_at
        FROM skels ORDER BY created_at DESC LIMIT ? OFFSET ?
    """

    SELECT_BY_ID = """
        SELECT id, skel_text, skel_char, skel_int, skel_float, skel_bool, skel_json, created_at, updated_at
        FROM skels WHERE id = ?
    """

    COUNT = "SELECT COUNT(*) FROM skels"

    UPDATE = """
        UPDATE skels
        SET skel_text = ?, skel_char = ?, skel_int = ?, skel_float = ?, skel_bool = ?, skel_json = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """

    DELETE = "DELETE FROM skels WHERE id = ?"

    @staticmethod
    def to_dict(row):
        if not row:
            return None
        return {
            "id": row[0],
            "skel_text": row[1],
            "skel_char": row[2],
            "skel_int": row[3],
            "skel_float": row[4],
            "skel_bool": bool(row[5]),
            "skel_json": row[6],
            "created_at": row[7] if len(row) > 7 else None,
            "updated_at": row[8] if len(row) > 8 else None,
        }
