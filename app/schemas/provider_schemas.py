from pydantic import BaseModel, ConfigDict
from typing import List
from app.schemas.appointment_schemas import Appointment

class ProviderBase(BaseModel):
    name: str
    specialty: str

class Provider(ProviderBase):
    id: int
    appointments: List[Appointment] = []

    model_config = ConfigDict(from_attributes=True)
