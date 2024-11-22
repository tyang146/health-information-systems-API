import re
from pydantic import BaseModel, field_validator
from datetime import date, time

class AppointmentBase(BaseModel):
    date: date
    time: time
    patient_id: int
    provider_id: int

    # Validator to ensure time is in HH:MM format
    @field_validator('time')
    def validate_time(cls, v):
        # Convert the time to string and strip extra precision if any
        time_str = v.isoformat()

        # Match the expected HH:MM format
        match = re.match(r"^(\d{2}):(\d{2})", time_str)
        if match:
            # Create a time object using only hours and minutes
            return time(hour=int(match.group(1)), minute=int(match.group(2)))
        
        raise ValueError('Time must be in the format HH:MM')

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        from_attributes = True
