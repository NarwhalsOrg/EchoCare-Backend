from pydantic import BaseModel, EmailStr, Field
from typing import Optional




class PatientData(BaseModel):
    ID: int
    HighBP: Optional[int] = Field(None, description="0 = no high BP, 1 = high BP")
    HighChol: Optional[int] = None
    CholCheck: Optional[int] = None
    BMI: Optional[float] = None
    Smoker: Optional[int] = None
    Stroke: Optional[int] = None
    HeartDiseaseorAttack: Optional[int] = None
    PhysActivity: Optional[int] = None
    Fruits: Optional[int] = None
    Veggies: Optional[int] = None
    HvyAlcoholConsump: Optional[int] = None
    AnyHealthcare: Optional[int] = None
    NoDocbcCost: Optional[int] = None
    GenHlth: Optional[int] = None
    MentHlth: Optional[int] = None
    PhysHlth: Optional[int] = None
    DiffWalk: Optional[int] = None
    Sex: Optional[int] = None
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None
