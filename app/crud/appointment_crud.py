from datetime import date, datetime, time, timedelta
from sqlalchemy.orm import Session
from app.models.appointment_models import Appointment
from app.models.patient_models import Patient
from app.models.provider_models import Provider
from app.schemas.appointment_schemas import AppointmentCreate, AppointmentUpdate
from fastapi import HTTPException, status

## helper function for appointments validation
def validate_appointment(
    db: Session,
    appointment_date: date,
    appointment_time: time,
    patient_id: int,
    provider_id: int,
    exclude_appointment_id: int = None
):
    # Check if the patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} does not exist."
        )

    # Check if the provider exists
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider with ID {provider_id} does not exist."
        )

    # Check if the date is not in the past
    today = datetime.today().date()
    if appointment_date < today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment date cannot be set in the past."
        )

    # Check if the time is within business hours
    business_start = time(9, 0)
    business_end = time(17, 0)
    if not (business_start <= appointment_time <= business_end):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointments must be scheduled between 9:00 AM and 5:00 PM."
        )

    # Check for conflicts for the patient
    appointment_datetime = datetime.combine(appointment_date, appointment_time)
    thirty_minutes_before = appointment_datetime - timedelta(minutes=30)
    thirty_minutes_after = appointment_datetime + timedelta(minutes=30)

    conflicting_patient_appointments = db.query(Appointment).filter(
        Appointment.id != exclude_appointment_id,  # Exclude the current appointment for updates
        Appointment.date == appointment_date,
        Appointment.patient_id == patient_id,
        Appointment.time >= thirty_minutes_before.time(),
        Appointment.time <= thirty_minutes_after.time()
    ).all()

    if conflicting_patient_appointments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This patient already has an appointment scheduled around this time. Ensure appointments are at least 30 minutes apart."
        )

    # Check for conflicts for the provider
    conflicting_provider_appointments = db.query(Appointment).filter(
        Appointment.id != exclude_appointment_id,  # Exclude the current appointment for updates
        Appointment.date == appointment_date,
        Appointment.provider_id == provider_id,
        Appointment.time >= thirty_minutes_before.time(),
        Appointment.time <= thirty_minutes_after.time()
    ).all()

    if conflicting_provider_appointments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An appointment already exists for this provider around this time. Choose a different time."
        )

def create_appointment(db: Session, appointment: AppointmentCreate):
    validate_appointment(
        db=db,
        appointment_date=appointment.date,
        appointment_time=appointment.time,
        patient_id=appointment.patient_id,
        provider_id=appointment.provider_id
    )

    # Create the appointment
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

def delete_appointment_by_id(db: Session, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        db.delete(appointment)
        db.commit()
        return appointment
    return None

def update_appointment_by_id(db: Session, appointment_id: int, appointment_data: AppointmentUpdate):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} does not exist."
        )
    
    validate_appointment(
        db=db,
        appointment_date=appointment_data.date,
        appointment_time=appointment_data.time,
        patient_id=appointment_data.patient_id,
        provider_id=appointment_data.provider_id,
        exclude_appointment_id=appointment_id
    )

    # Update the fields
    for field, value in appointment_data.model_dump(exclude_unset=True).items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)
    return appointment