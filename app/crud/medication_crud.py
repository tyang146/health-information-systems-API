from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.medication_models import Medication
from app.models.patient_models import Patient
from app.schemas.medication_schemas import MedicationCreate

def create_medication(db: Session, medication: MedicationCreate):
    # Check if the patient exists
    patient = db.query(Patient).filter(Patient.id == medication.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {medication.patient_id} does not exist."
        )
    
    # If no conflicts, create the medication
    db_medication = Medication(name=medication.name, dosage=medication.dosage, patient_id=medication.patient_id)
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

def get_medication_by_id(db: Session, medication_id: int):
    return db.query(Medication).filter(Medication.id == medication_id).first()

def get_all_medications(db: Session):
    return db.query(Medication).all()
