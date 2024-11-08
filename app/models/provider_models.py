from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_models import Base, BaseModel

class Provider(Base, BaseModel):
    __tablename__ = "providers"
    
    name = Column(String, index=True)
    specialty = Column(String)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="provider", cascade="all, delete-orphan")
