from pydantic import BaseModel
from datetime import datetime

class AppointmentBase(BaseModel):
    date_time: datetime

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    patient_id: int
    provider_id: int

    class Config:
        from_attributes = True
