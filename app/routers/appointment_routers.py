from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.schemas.appointment_schemas import Appointment, AppointmentCreate, AppointmentUpdate
from app.crud.appointment_crud import create_appointment, delete_appointment_by_id, get_appointments_by_date, get_all_appointments, update_appointment_by_id

router = APIRouter()

@router.post("/", response_model=Appointment, dependencies=[Depends(get_current_user)])
def create_new_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return create_appointment(db=db, appointment=appointment)

@router.get("/{appointment_date}", response_model=List[Appointment])
def read_appointments_by_date(appointment_date: date, db: Session = Depends(get_db)):
    appointments = get_appointments_by_date(db=db, appointment_date=appointment_date)
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this date.")
    return appointments

@router.get("/", response_model=List[Appointment])
def read_appointments(db: Session = Depends(get_db)):
    return get_all_appointments(db=db)

@router.delete("/{appointment_id}", response_model=Appointment, dependencies=[Depends(get_current_user)])
def cancel_appointment_by_id(appointment_id: int, db: Session = Depends(get_db)):
    appointment = delete_appointment_by_id(db=db, appointment_id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return appointment

@router.put("/{appointment_id}", response_model=Appointment, dependencies=[Depends(get_current_user)])
def change_appointment_by_id(appointment_id: int, appointment_data: AppointmentUpdate, db: Session = Depends(get_db)):
    updated_appointment = update_appointment_by_id(db=db, appointment_id=appointment_id, appointment_data=appointment_data)
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return updated_appointment

