from sqlalchemy import Column, Date, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.models.base_models import Base, BaseModel

class Appointment(Base, BaseModel):
    __tablename__ = "appointments"
    
    patient_id = Column(Integer, ForeignKey("patients.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    date = Column(Date)
    time = Column(Time)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    provider = relationship("Provider", back_populates="appointments")
