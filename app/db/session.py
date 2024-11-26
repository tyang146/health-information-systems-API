from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base_models import Base 

DATABASE_URL = "sqlite:///./healthcare.db"

# boiler plate code to initialize the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create the database tables using models that inherit from Base model
def init_db():
    Base.metadata.create_all(bind=engine)  

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()