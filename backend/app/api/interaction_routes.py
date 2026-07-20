from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.interaction import (
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse,
)
from app.services import interaction_service

router = APIRouter(
    prefix="/interactions",
    tags=["Interactions"]
)


@router.post("/", response_model=InteractionResponse)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    return interaction_service.create_interaction(db, interaction)


@router.get("/", response_model=list[InteractionResponse])
def get_all_interactions(db: Session = Depends(get_db)):
    return interaction_service.get_all_interactions(db)


@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = interaction_service.get_interaction(db, interaction_id)

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    return interaction


@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(
    interaction_id: int,
    interaction: InteractionUpdate,
    db: Session = Depends(get_db)
):
    updated = interaction_service.update_interaction(
        db,
        interaction_id,
        interaction
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Interaction not found")

    return updated


@router.delete("/{interaction_id}")
def delete_interaction(
    interaction_id: int,
    db: Session = Depends(get_db)
):
    deleted = interaction_service.delete_interaction(db, interaction_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Interaction not found")

    return {"message": "Interaction deleted successfully"}