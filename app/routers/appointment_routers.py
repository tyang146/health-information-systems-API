from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.appointment_schemas import Appointment, AppointmentCreate
from app.crud.appointment_crud import create_appointment, get_appointment_by_id, get_all_appointments

router = APIRouter()

@router.post("/", response_model=Appointment)
def create_new_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return create_appointment(db=db, appointment=appointment)

@router.get("/{appointment_id}", response_model=Appointment)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = get_appointment_by_id(db=db, appointment_id=appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.get("/", response_model=List[Appointment])
def read_appointments(db: Session = Depends(get_db)):
    return get_all_appointments(db=db)
