from sqlalchemy.orm import Session
from app.models.appointment_models import Appointment
from app.schemas.appointment_schemas import AppointmentCreate

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(
        appointment_time=appointment.appointment_time,
        patient_id=appointment.patient_id,
        provider_id=appointment.provider_id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def get_all_appointments(db: Session):
    return db.query(Appointment).all()
