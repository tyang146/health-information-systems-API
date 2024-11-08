from sqlalchemy.orm import Session
from app.models.patient_models import Patient
from app.schemas.patient_schemas import PatientCreate

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(name=patient.name, age=patient.age, gender=patient.gender)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_all_patients(db: Session):
    return db.query(Patient).all()

def get_patient_by_name(db: Session, name: str):
    return db.query(Patient).filter(Patient.name.ilike(f"%{name}%")).all()
