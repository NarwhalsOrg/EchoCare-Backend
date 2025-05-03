from pydantic import BaseModel, EmailStr, Field


class PredictionResult(BaseModel):
    prediction: int
    probability: float
    probability_percent: str
    prediction_label: str
    explanations: list[str]
