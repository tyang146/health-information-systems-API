from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from app.models.appointment_models import Appointment
from app.models.patient_models import Patient
from app.models.provider_models import Provider
from app.schemas.appointment_schemas import AppointmentCreate
from fastapi import HTTPException, status

def create_appointment(db: Session, appointment: AppointmentCreate):
    # Check if the patient exists
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {appointment.patient_id} does not exist."
        )

    # Check if the provider exists
    provider = db.query(Provider).filter(Provider.id == appointment.provider_id).first()
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider with ID {appointment.provider_id} does not exist."
        )

    # **Validate that the appointment date is not in the past during creation**
    today = datetime.today().date()
    if appointment.date < today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment date cannot be in the past."
        )

    # Combine the date and time into a full datetime object for comparison
    appointment_datetime = datetime.combine(appointment.date, appointment.time)

    # Check if an appointment already exists at the same time
    conflicting_appointments = db.query(Appointment).filter(
        Appointment.date == appointment.date,
        Appointment.time == appointment.time
    ).all()

    if conflicting_appointments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An appointment already exists at the same time."
        )

    # Ensure appointments are at least 30 minutes apart
    thirty_minutes_before = appointment_datetime - timedelta(minutes=30)
    thirty_minutes_after = appointment_datetime + timedelta(minutes=30)

    conflicting_appointments_within_timeframe = db.query(Appointment).filter(
        (Appointment.date == appointment.date) &
        (Appointment.time >= thirty_minutes_before.time()) &
        (Appointment.time <= thirty_minutes_after.time())
    ).all()

    if conflicting_appointments_within_timeframe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointments must be at least 30 minutes apart."
        )

    # If no conflicts, create the appointment
    db_appointment = Appointment(
        date=appointment.date,
        time=appointment.time,
        patient_id=appointment.patient_id,
        provider_id=appointment.provider_id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment

def get_appointments_by_date(db: Session, appointment_date: date):
    return db.query(Appointment).filter(Appointment.date == appointment_date).all()


def get_all_appointments(db: Session):
    return db.query(Appointment).all()
