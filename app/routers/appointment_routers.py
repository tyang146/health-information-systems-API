from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.schemas.appointment_schemas import Appointment, AppointmentCreate
from app.crud.appointment_crud import create_appointment, get_appointments_by_date, get_all_appointments

router = APIRouter()

@router.post("/", response_model=Appointment, dependencies=[Depends(get_current_user)])
def create_new_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return create_appointment(db=db, appointment=appointment)

@router.get("/by_date", response_model=List[Appointment])
def get_appointments_by_date_route(appointment_date: date, db: Session = Depends(get_db)):
    appointments = get_appointments_by_date(db=db, appointment_date=appointment_date)
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this date.")
    
    return appointments

@router.get("/", response_model=List[Appointment])
def read_appointments(db: Session = Depends(get_db)):
    return get_all_appointments(db=db)
