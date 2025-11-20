from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import adbutils

router = APIRouter(prefix="/adb", tags=["adb"])


class AdbRequest(BaseModel):
    cmd: str = Field(..., min_length=1)
    serial: str | None = None
    timeout: int | None = None


@router.post("/")
def execute(req: AdbRequest):
    """Execute ADB shell command"""
    try:
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        device = adb.device(serial=req.serial) if req.serial else adb.device_list()[0]
        result = device.shell2(req.cmd, timeout=req.timeout)

        return {
            "success": result.returncode == 0,
            "output": result.output.strip() if result.output else None,
            "returncode": result.returncode,
            "serial": device.serial,
        }
    except IndexError:
        raise HTTPException(404, "No devices connected")
    except adbutils.AdbError as e:
        raise HTTPException(500, f"ADB error: {str(e)}")


@router.get("/devices")
def devices():
    """List connected devices"""
    try:
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        return {"devices": [{"serial": d.serial, "state": d.state} for d in adb.device_list()]}
    except Exception as e:
        raise HTTPException(500, str(e))
