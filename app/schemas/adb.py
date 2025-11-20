from pydantic import BaseModel, Field


class AdbRequest(BaseModel):
    cmd: str = Field(..., min_length=1)
    serial: str | None = None
    timeout: int | None = None


class AdbResponse(BaseModel):
    success: bool
    output: str | None
    returncode: int
    serial: str
