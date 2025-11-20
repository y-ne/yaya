import subprocess
from app.schemas.shell import ShellRequest, ShellResponse


class ShellService:
    def execute(self, req: ShellRequest) -> ShellResponse:
        try:
            result = subprocess.run(
                req.cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=req.timeout
            )

            return ShellResponse(
                success=result.returncode == 0,
                output=result.stdout.strip() if result.stdout else None,
                error=result.stderr.strip() if result.stderr else None,
                returncode=result.returncode,
            )
        except subprocess.TimeoutExpired:
            return ShellResponse(
                success=False,
                output=None,
                error=f"Command timed out after {req.timeout} seconds",
                returncode=-1,
            )
        except Exception as e:
            return ShellResponse(
                success=False,
                output=None,
                error=str(e),
                returncode=-1,
            )
