from sqlalchemy import Column, String
from app.models.base_models import Base, BaseModel

class User(Base, BaseModel):
    __tablename__ = "users"
    
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
