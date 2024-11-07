from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base_models import Base 

DATABASE_URL = "sqlite:///./healthcare.db"

# initialize the database engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database tables
def init_db():
    Base.metadata.create_all(bind=engine)  

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()