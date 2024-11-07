from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.provider_schemas import Provider, ProviderCreate
from app.crud.provider_crud import create_provider, get_provider_by_id, get_all_providers

router = APIRouter()

@router.post("/", response_model=Provider)
def create_new_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    return create_provider(db=db, provider=provider)

@router.get("/{provider_id}", response_model=Provider)
def read_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = get_provider_by_id(db=db, provider_id=provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.get("/", response_model=List[Provider])
def read_providers(db: Session = Depends(get_db)):
    return get_all_providers(db=db)
