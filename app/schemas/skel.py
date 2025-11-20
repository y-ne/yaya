from pydantic import BaseModel, Field, ConfigDict


class SkelBase(BaseModel):
    skel_text: str = Field(min_length=1, max_length=1000)
    skel_char: str | None = Field(None, max_length=255)
    skel_int: int | None = None
    skel_float: float | None = None
    skel_bool: bool = False
    skel_json: dict | list | None = None


class SkelCreate(SkelBase):
    pass


class SkelUpdate(BaseModel):
    skel_text: str | None = Field(None, min_length=1, max_length=1000)
    skel_char: str | None = Field(None, max_length=255)
    skel_int: int | None = None
    skel_float: float | None = None
    skel_bool: bool | None = None
    skel_json: dict | list | None = None


class SkelResponse(SkelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SkelList(BaseModel):
    skels: list[SkelResponse]
    total: int
    page: int
    page_size: int
