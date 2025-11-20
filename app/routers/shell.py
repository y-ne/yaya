from fastapi import APIRouter

from app.schemas.shell import ShellRequest, ShellResponse
from app.services.shell_service import ShellService

router = APIRouter(prefix="/shell", tags=["shell"])


def get_service():
    return ShellService()


@router.post("/", response_model=ShellResponse)
def execute_command(req: ShellRequest):
    """Execute shell command on the server"""
    service = get_service()
    return service.execute(req)
