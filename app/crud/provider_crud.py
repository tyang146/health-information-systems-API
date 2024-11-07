from sqlalchemy.orm import Session
from app.models.provider_models import Provider
from app.schemas.provider_schemas import ProviderCreate

def create_provider(db: Session, provider: ProviderCreate):
    db_provider = Provider(name=provider.name, specialty=provider.specialty)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

def get_provider_by_id(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()

def get_all_providers(db: Session):
    return db.query(Provider).all()
