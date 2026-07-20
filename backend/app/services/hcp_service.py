from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate


def create_hcp(db: Session, hcp: HCPCreate):
    db_hcp = HCP(**hcp.model_dump())

    try:
        db.add(db_hcp)
        db.commit()
        db.refresh(db_hcp)
        return db_hcp

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="An HCP with this email already exists."
        )


def get_all_hcps(db: Session):
    return db.query(HCP).all()


def get_hcp(db: Session, hcp_id: int):
    return (
        db.query(HCP)
        .filter(HCP.id == hcp_id)
        .first()
    )


def update_hcp(
    db: Session,
    hcp_id: int,
    hcp: HCPUpdate
):
    db_hcp = get_hcp(db, hcp_id)

    if not db_hcp:
        return None

    for key, value in hcp.model_dump().items():
        setattr(db_hcp, key, value)

    try:
        db.commit()
        db.refresh(db_hcp)
        return db_hcp

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="An HCP with this email already exists."
        )


def delete_hcp(db: Session, hcp_id: int):
    db_hcp = get_hcp(db, hcp_id)

    if not db_hcp:
        return None

    db.delete(db_hcp)
    db.commit()

    return db_hcp