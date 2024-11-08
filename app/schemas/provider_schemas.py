from pydantic import BaseModel
from typing import List
from app.schemas.appointment_schemas import Appointment

class ProviderBase(BaseModel):
    name: str
    specialty: str

class Provider(ProviderBase):
    id: int
    appointments: List[Appointment] = []

    class Config:
        from_attributes = True
