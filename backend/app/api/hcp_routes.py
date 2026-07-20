from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPResponse
from app.services import hcp_service

router = APIRouter(
    prefix="/hcps",
    tags=["Healthcare Professionals"]
)


@router.post("/", response_model=HCPResponse)
def create_hcp(hcp: HCPCreate, db: Session = Depends(get_db)):
    return hcp_service.create_hcp(db, hcp)


@router.get("/", response_model=list[HCPResponse])
def get_all_hcps(db: Session = Depends(get_db)):
    return hcp_service.get_all_hcps(db)


@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    hcp = hcp_service.get_hcp(db, hcp_id)

    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    return hcp


@router.put("/{hcp_id}", response_model=HCPResponse)
def update_hcp(
    hcp_id: int,
    hcp: HCPUpdate,
    db: Session = Depends(get_db)
):
    updated = hcp_service.update_hcp(db, hcp_id, hcp)

    if not updated:
        raise HTTPException(status_code=404, detail="HCP not found")

    return updated


@router.delete("/{hcp_id}")
def delete_hcp(hcp_id: int, db: Session = Depends(get_db)):
    deleted = hcp_service.delete_hcp(db, hcp_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="HCP not found")

    return {"message": "HCP deleted successfully"}