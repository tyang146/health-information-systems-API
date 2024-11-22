from datetime import date
from typing import List, Literal
from pydantic import BaseModel, field_validator
from app.schemas.appointment_schemas import Appointment
import re

class PatientBase(BaseModel):
    name: str
    date_of_birth: date  
    gender: Literal['male', 'female', 'other']  # Restrict gender to specific values
    phone_number: str

    # Validator for date_of_birth
    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 0:
            raise ValueError("date_of_birth cannot be in the future.")
        if age > 120:
            raise ValueError("Patient age cannot exceed 120 years.")
        return value

    # Validator for phone_number
    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        # Regex pattern for phone numbers (e.g., +11234567890 or 1234567890)
        phone_pattern = re.compile(r"^\+?1?\d{10,15}$")
        if not phone_pattern.match(value):
            raise ValueError(
                "phone_number must be a valid phone number (e.g., +11234567890 or 1234567890)."
            )
        return value


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int
    appointments: List[Appointment] = []

    class Config:
        from_attributes = True
