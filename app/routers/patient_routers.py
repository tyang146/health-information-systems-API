from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.patient_models import Patient
from app.schemas.patient_schemas import PatientCreate, Patient
from app.crud.patient_crud import create_patient, get_all_patients, get_patient_by_id, get_patient_by_name

router = APIRouter()

# Create a new patient
@router.post("/", response_model=Patient, dependencies=[Depends(get_current_user)])
def create_new_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db=db, patient=patient)

# Get all patients
@router.get("/", response_model=List[Patient])
def read_patients(db: Session = Depends(get_db)):
    patients = get_all_patients(db=db)
    return patients

# Get a specific patient by ID
@router.get("/{patient_id}", response_model=Patient)
def read_patient_by_id(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient_by_id(db=db, patient_id=patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Get patients by name
@router.get("/path_parameters_search/{name}", response_model=list[Patient])
def read_patients_by_name(name: str, db: Session = Depends(get_db)):
    providers = get_patient_by_name(db=db, name=name)
    if not providers:
        raise HTTPException(status_code=404, detail="Patient not found")
    return providers