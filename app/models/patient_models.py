from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.models.base_models import Base, BaseModel

class Patient(Base, BaseModel):
    __tablename__ = "patients"
    
    name = Column(String, index=True)
    date_of_birth = Column(Date)
    gender = Column(String)
    phone_number = Column(String)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
