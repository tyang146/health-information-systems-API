from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.provider_schemas import Provider
from app.crud.provider_crud import get_providers

router = APIRouter()

@router.get("/{provider_id}", response_model=Provider)
def read_provider_by_id(provider_id: int, db: Session = Depends(get_db)):
    provider = get_providers(db=db, provider_id=provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.get("/query_parameters_search/providers", response_model=list[Provider])
def read_providers(db: Session = Depends(get_db), name: str = None, specialty: str = None):
    providers = get_providers(db=db, name=name, specialty=specialty)
    if not providers:
        raise HTTPException(status_code=404, detail="No providers found matching the criteria")
    return providers
