from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_models import Base, BaseModel

class Patient(Base, BaseModel):
    __tablename__ = "patients"
    
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    
    # Relationships
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
