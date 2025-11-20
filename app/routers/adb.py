from fastapi import APIRouter, HTTPException, status
import adbutils

from app.schemas.adb import AdbRequest, AdbResponse
from app.services.adb_service import AdbService

router = APIRouter(prefix="/adb", tags=["adb"])


def get_service():
    return AdbService()


@router.post("/", response_model=AdbResponse)
def execute_command(req: AdbRequest):
    service = get_service()
    try:
        return service.execute(req)
    except IndexError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No devices connected")
    except adbutils.AdbError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ADB error: {str(e)}")


@router.get("/devices")
def list_devices():
    service = get_service()
    try:
        devices = service.list_devices()
        return {"devices": devices, "count": len(devices)}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
