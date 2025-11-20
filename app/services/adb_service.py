import adbutils
from app.schemas.adb import AdbRequest, AdbResponse


class AdbService:
    def __init__(self, host: str = "127.0.0.1", port: int = 5037):
        self.adb = adbutils.AdbClient(host=host, port=port)

    def execute(self, req: AdbRequest) -> AdbResponse:
        device = self.adb.device(serial=req.serial) if req.serial else self.adb.device_list()[0]
        result = device.shell2(req.cmd, timeout=req.timeout)

        return AdbResponse(
            success=result.returncode == 0,
            output=result.output.strip() if result.output else None,
            returncode=result.returncode,
            serial=device.serial,
        )

    def list_devices(self) -> list[dict]:
        return [{"serial": d.serial, "state": d.state} for d in self.adb.device_list()]
