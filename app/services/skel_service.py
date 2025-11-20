import json
from app.models.skel import SkelModel
from app.schemas.skel import SkelCreate, SkelUpdate


class SkelService:
    def __init__(self, db):
        self.db = db
        self.model = SkelModel

    def create_table(self):
        self.db.execute(self.model.CREATE_TABLE)
        self.db.commit()

    def create(self, skel: SkelCreate):
        cursor = self.db.execute(
            self.model.INSERT,
            [
                skel.skel_text,
                skel.skel_char,
                skel.skel_int,
                skel.skel_float,
                int(skel.skel_bool),
                json.dumps(skel.skel_json) if skel.skel_json else None
            ]
        )
        self.db.commit()
        return self.get_by_id(cursor.lastrowid)

    def get_all(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        result = self.db.execute(self.model.SELECT_ALL, [page_size, offset])
        skels = [self._parse_row(row) for row in result.fetchall()]
        total = self.db.execute(self.model.COUNT).fetchone()[0]
        return skels, total

    def get_by_id(self, skel_id: int):
        result = self.db.execute(self.model.SELECT_BY_ID, [skel_id])
        row = result.fetchone()
        return self._parse_row(row)

    def update(self, skel_id: int, skel_update: SkelUpdate):
        existing = self.get_by_id(skel_id)
        if not existing:
            return None

        updated = {**existing, **skel_update.model_dump(exclude_unset=True)}
        self.db.execute(
            self.model.UPDATE,
            [
                updated["skel_text"],
                updated["skel_char"],
                updated["skel_int"],
                updated["skel_float"],
                int(updated["skel_bool"]),
                json.dumps(updated["skel_json"]) if updated["skel_json"] else None,
                skel_id
            ]
        )
        self.db.commit()
        return self.get_by_id(skel_id)

    def delete(self, skel_id: int):
        if not self.get_by_id(skel_id):
            return False
        self.db.execute(self.model.DELETE, [skel_id])
        self.db.commit()
        return True

    def _parse_row(self, row):
        if not row:
            return None
        data = self.model.to_dict(row)
        if data and data.get("skel_json"):
            try:
                data["skel_json"] = json.loads(data["skel_json"])
            except (json.JSONDecodeError, TypeError):
                data["skel_json"] = None
        return data
