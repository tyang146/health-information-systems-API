from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_models import Base, BaseModel

class Medication(Base, BaseModel):
    __tablename__ = "medications"
    
    name = Column(String)
    dosage = Column(String)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # Relationships
    patient = relationship("Patient", back_populates="medications")
