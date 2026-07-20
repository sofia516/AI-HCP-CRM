from pydantic import BaseModel, EmailStr
from typing import Optional


class HCPBase(BaseModel):
    name: str
    specialty: str
    hospital: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class HCPCreate(HCPBase):
    pass


class HCPUpdate(HCPBase):
    pass


class HCPResponse(HCPBase):
    id: int

    class Config:
        from_attributes = True