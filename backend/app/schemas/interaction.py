from pydantic import BaseModel
from datetime import datetime


class InteractionBase(BaseModel):
    hcp_id: int
    interaction_type: str
    notes: str


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(InteractionBase):
    pass


class InteractionResponse(InteractionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True