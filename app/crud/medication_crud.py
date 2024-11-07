from sqlalchemy.orm import Session
from app.models.medication_models import Medication
from app.schemas.medication_schemas import MedicationCreate

def create_medication(db: Session, medication: MedicationCreate):
    db_medication = Medication(name=medication.name, dosage=medication.dosage, patient_id=medication.patient_id)
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

def get_medication_by_id(db: Session, medication_id: int):
    return db.query(Medication).filter(Medication.id == medication_id).first()

def get_all_medications(db: Session):
    return db.query(Medication).all()
