from pydantic import BaseModel, Field
from typing import List, Literal
from app.schemas.appointment_schemas import Appointment
from app.schemas.medication_schemas import Medication

class PatientBase(BaseModel):
    name: str
    age: int = Field(..., gt=0, lt=200)  # Apply constraints using Field
    gender: Literal['male', 'female', 'other']  # Restrict gender to 'male', 'female', or 'other'

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    medications: List[Medication] = [] 
    appointments: List[Appointment] = []

    class Config:
        from_attributes = True
