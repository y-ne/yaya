from pydantic import BaseModel, Field


class AdbCommandRequest(BaseModel):
    cmd: str = Field(..., min_length=1, description="ADB shell command to execute")
    serial: str | None = Field(None, description="Device serial number (optional, uses first device if not specified)")
    timeout: int | None = Field(None, ge=1, description="Command timeout in seconds")


class AdbCommandResponse(BaseModel):
    success: bool
    output: str | None = None
    error: str | None = None
    returncode: int | None = None
    device_serial: str | None = None
