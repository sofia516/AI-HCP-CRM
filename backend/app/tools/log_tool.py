from sqlalchemy.orm import Session
from app.models.interaction import Interaction


def log_interaction(
    db: Session,
    hcp_id: int,
    interaction_type: str,
    notes: str
):
    interaction = Interaction(
        hcp_id=hcp_id,
        interaction_type=interaction_type,
        notes=notes
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return {
        "status": "success",
        "interaction_id": interaction.id,
        "message": "Interaction logged successfully."
    }