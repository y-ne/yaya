from fastapi import APIRouter, HTTPException, status

from app.schemas.adb import AdbCommandRequest, AdbCommandResponse
from app.services.adb_service import AdbService

router = APIRouter(prefix="/adb", tags=["adb"])


def get_adb_service():
    return AdbService()


@router.post("/", response_model=AdbCommandResponse)
def execute_adb_command(request: AdbCommandRequest):
    """
    Execute an ADB shell command on a connected Android device.

    - **cmd**: The shell command to execute (required)
    - **serial**: Device serial number (optional, uses first device if not specified)
    - **timeout**: Command timeout in seconds (optional)
    """
    service = get_adb_service()
    result = service.execute_command(
        cmd=request.cmd,
        serial=request.serial,
        timeout=request.timeout
    )
    return result


@router.get("/devices")
def list_devices():
    """
    List all connected Android devices.
    """
    service = get_adb_service()
    try:
        devices = service.list_devices()
        return {"devices": devices, "count": len(devices)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
