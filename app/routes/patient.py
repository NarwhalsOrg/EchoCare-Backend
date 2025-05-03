from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.PatientData import PatientData
from app.schemas.ChatHistory import ChatRequest
from app.core.database import get_db
from app.controllers.PatientController import create_patient_data, get_patient_data
from app.controllers.ChatControllers import get_chat_history
from app.service.ml.predict import predict_and_explain
from app.auth.deps import get_current_user

router = APIRouter()

@router.post("/upload_data")
def upload_data(
    patient: PatientData,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Save or update patient data
    create_patient_data(db, user.user_id, patient.dict(exclude={"ID"}))
    return {"status": "success"}

@router.get("/patient_data")
def get_data(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    pdata = get_patient_data(db, user.user_id)
    if not pdata:
        raise HTTPException(404, "No patient data found.")
    return pdata

@router.get("/chat_history/{session_id}")
def chat_history(
    session_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    history = get_chat_history(db, user.user_id, session_id)
    return [
        {"sender": msg.sender, "message": msg.message, "timestamp": msg.timestamp}
        for msg in history
    ]

@router.post("/predict")
def predict(
    patient: PatientData,
    user=Depends(get_current_user)
):
    # Returns ML prediction and explanations
    result = predict_and_explain(patient.dict(exclude={"ID"}))
    return result
