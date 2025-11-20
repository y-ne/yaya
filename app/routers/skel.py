from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.database import get_db
from app.schemas.skel import SkelCreate, SkelUpdate, SkelResponse, SkelList
from app.services.skel_service import SkelService

router = APIRouter(prefix="/skels", tags=["skels"])


def get_service(db=Depends(get_db)):
    return SkelService(db)


@router.post("/", response_model=SkelResponse, status_code=status.HTTP_201_CREATED)
def create_skel(skel: SkelCreate, service: SkelService = Depends(get_service)):
    return service.create(skel)


@router.get("/", response_model=SkelList)
def get_skels(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: SkelService = Depends(get_service)
):
    skels, total = service.get_all(page, page_size)
    return {"skels": skels, "total": total, "page": page, "page_size": page_size}


@router.get("/{skel_id}", response_model=SkelResponse)
def get_skel(skel_id: int, service: SkelService = Depends(get_service)):
    skel = service.get_by_id(skel_id)
    if not skel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Skel {skel_id} not found")
    return skel


@router.put("/{skel_id}", response_model=SkelResponse)
def update_skel(
    skel_id: int,
    skel_update: SkelUpdate,
    service: SkelService = Depends(get_service)
):
    skel = service.update(skel_id, skel_update)
    if not skel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Skel {skel_id} not found")
    return skel


@router.delete("/{skel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skel(skel_id: int, service: SkelService = Depends(get_service)):
    if not service.delete(skel_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Skel {skel_id} not found")
