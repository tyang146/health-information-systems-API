from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.provider_schemas import Provider
from app.crud.provider_crud import get_providers

router = APIRouter()

@router.get("/query_parameters_search/providers", response_model=list[Provider])
def read_providers(db: Session = Depends(get_db), name: str = None, specialty: str = None):
    # Call the CRUD function to get providers with the filters applied
    providers = get_providers(db=db, name=name, specialty=specialty)
    
    if not providers:
        raise HTTPException(status_code=404, detail="No providers found matching the criteria")
    
    return providers
