from sqlalchemy.orm import Session
from app.models.provider_models import Provider

def get_provider_by_id(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()

def get_providers(db: Session, name: str = None, specialty: str = None):
    query = db.query(Provider)

    # Apply filters if the query parameters are provided
    if name:
        query = query.filter(Provider.name.ilike(f"%{name}%"))
    if specialty:
        query = query.filter(Provider.specialty.ilike(f"%{specialty}%"))

    return query.all()