from pydantic import BaseModel, Field


class ShellRequest(BaseModel):
    cmd: str = Field(..., min_length=1)
    timeout: int | None = Field(30, ge=1, le=300)


class ShellResponse(BaseModel):
    success: bool
    output: str | None
    error: str | None
    returncode: int
