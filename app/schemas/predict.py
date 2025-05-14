from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    name: str = Field(..., example="John Doe")
    HighBP: int = Field(..., example=1)
    HighChol: int = Field(..., example=1)
    HeartDiseaseorAttack: int = Field(..., example=0)
    Stroke: int = Field(..., example=0)
    Smoker: int = Field(..., example=1)
    PhysActivity: int = Field(..., example=1)
    DiffWalk: int = Field(..., example=0)
    BMI: float = Field(..., example=27.5)
    MentHlth: int = Field(..., example=5)
    PhysHlth: int = Field(..., example=10)
    GenHlth: int = Field(..., example=3)
    Sex: int = Field(..., example=1)
    Age: int = Field(..., example=50)
    HvyAlcoholConsump: int = Field(..., example=0)

    def to_feature_list(self):
        return [
            self.HighBP, self.HighChol, self.HeartDiseaseorAttack,
            self.Stroke, self.Smoker, self.PhysActivity, self.DiffWalk,
            self.BMI, self.MentHlth, self.PhysHlth, self.GenHlth,
            self.Sex, self.Age, self.HvyAlcoholConsump
        ]

class PredictResponse(BaseModel):
    name: str
    prediction: str
    probability: float
    explanation: List[str]
