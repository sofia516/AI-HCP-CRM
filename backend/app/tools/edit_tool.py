from sqlalchemy.orm import Session
from app.models.interaction import Interaction


def edit_interaction(
    db: Session,
    interaction_id: int,
    interaction_type: str,
    notes: str
):
    interaction = (
        db.query(Interaction)
        .filter(Interaction.id == interaction_id)
        .first()
    )

    if not interaction:
        return {
            "status": "error",
            "message": "Interaction not found."
        }

    interaction.interaction_type = interaction_type
    interaction.notes = notes

    db.commit()
    db.refresh(interaction)

    return {
        "status": "success",
        "message": "Interaction updated successfully."
    }