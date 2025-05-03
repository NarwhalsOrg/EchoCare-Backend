from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class PatientData(Base):
    __tablename__ = "patient_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False)
    HighBP = Column(Integer)
    HighChol = Column(Integer)
    CholCheck = Column(Integer)
    BMI = Column(Float)
    Smoker = Column(Integer)
    Stroke = Column(Integer)
    HeartDiseaseorAttack = Column(Integer)
    PhysActivity = Column(Integer)
    Fruits = Column(Integer)
    Veggies = Column(Integer)
    HvyAlcoholConsump = Column(Integer)
    AnyHealthcare = Column(Integer)
    NoDocbcCost = Column(Integer)
    GenHlth = Column(Integer)
    MentHlth = Column(Integer)
    PhysHlth = Column(Integer)
    DiffWalk = Column(Integer)
    Sex = Column(Integer)
    Age = Column(Integer)
    Education = Column(Integer)
    Income = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="patient_data")

