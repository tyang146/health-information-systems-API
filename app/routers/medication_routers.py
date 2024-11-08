from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.schemas.medication_schemas import Medication, MedicationCreate
from app.crud.medication_crud import create_medication, get_medication_by_id, get_all_medications

router = APIRouter()

@router.post("/", response_model=Medication, dependencies=[Depends(get_current_user)])
def create_new_medication(medication: MedicationCreate, db: Session = Depends(get_db)):
    return create_medication(db=db, medication=medication)

@router.get("/{medication_id}", response_model=Medication)
def read_medication(medication_id: int, db: Session = Depends(get_db)):
    medication = get_medication_by_id(db=db, medication_id=medication_id)
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication

@router.get("/", response_model=List[Medication])
def read_medications(db: Session = Depends(get_db)):
    return get_all_medications(db=db)
