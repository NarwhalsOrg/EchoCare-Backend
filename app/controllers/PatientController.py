from sqlalchemy.orm import Session
from app.models.PatientData import PatientData


def create_patient_data(db: Session, user_id: str, data: dict):
    db_patient = PatientData(user_id=user_id, **data)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient_data(db: Session, user_id: str):
    return db.query(PatientData).filter(PatientData.user_id == user_id).order_by(PatientData.created_at.desc()).first()
