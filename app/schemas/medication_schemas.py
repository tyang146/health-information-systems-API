from pydantic import BaseModel

class MedicationBase(BaseModel):
    name: str
    dosage: str
    patient_id: int

class MedicationCreate(MedicationBase):
    pass

class Medication(MedicationBase):
    id: int

    class Config:
        from_attributes = True
