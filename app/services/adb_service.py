import adbutils
from adbutils import AdbError, AdbTimeout


class AdbService:
    def __init__(self, host: str = "127.0.0.1", port: int = 5037):
        self.adb = adbutils.AdbClient(host=host, port=port)

    def execute_command(self, cmd: str, serial: str | None = None, timeout: int | None = None) -> dict:
        """
        Execute an ADB shell command on a device.

        Args:
            cmd: The shell command to execute
            serial: Device serial number (optional, uses first device if not specified)
            timeout: Command timeout in seconds

        Returns:
            Dictionary with execution results
        """
        try:
            # Get device
            if serial:
                device = self.adb.device(serial=serial)
            else:
                # Get first available device
                devices = self.adb.device_list()
                if not devices:
                    return {
                        "success": False,
                        "error": "No devices connected",
                        "output": None,
                        "returncode": None,
                        "device_serial": None,
                    }
                device = devices[0]

            # Execute command with shell2 to get returncode
            result = device.shell2(cmd, timeout=timeout)

            return {
                "success": result.returncode == 0,
                "output": result.output.strip() if result.output else None,
                "error": None if result.returncode == 0 else result.output.strip(),
                "returncode": result.returncode,
                "device_serial": device.serial,
            }

        except AdbTimeout:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds",
                "output": None,
                "returncode": None,
                "device_serial": serial,
            }
        except AdbError as e:
            return {
                "success": False,
                "error": f"ADB error: {str(e)}",
                "output": None,
                "returncode": None,
                "device_serial": serial,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "output": None,
                "returncode": None,
                "device_serial": serial,
            }

    def list_devices(self) -> list[dict]:
        """List all connected devices."""
        try:
            devices = self.adb.device_list()
            return [
                {
                    "serial": device.serial,
                    "state": device.state,
                }
                for device in devices
            ]
        except Exception as e:
            raise Exception(f"Failed to list devices: {str(e)}")
