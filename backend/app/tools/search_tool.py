from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.interaction import Interaction


def search_interactions(db: Session, keyword: str):
    interactions = (
        db.query(Interaction)
        .filter(
            or_(
                Interaction.notes.ilike(f"%{keyword}%"),
                Interaction.interaction_type.ilike(f"%{keyword}%"),
            )
        )
        .all()
    )

    return interactions