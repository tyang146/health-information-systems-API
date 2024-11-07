from pydantic import BaseModel
from typing import List
from app.schemas.appointment_schemas import Appointment
from app.schemas.medication_schemas import Medication

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    medications: List[Medication] = [] 
    appointments: List[Appointment] = []

    class Config:
        from_attributes = True