from pydantic import BaseModel

class MedicationBase(BaseModel):
    name: str
    dosage: str

class MedicationCreate(MedicationBase):
    pass

class Medication(MedicationBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True
