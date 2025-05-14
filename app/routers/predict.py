from fastapi import APIRouter, HTTPException, Request
from app.schemas.predict import PredictRequest, PredictResponse   # not able to import
from app.services.ml.model_loader import get_model_components
from app.services.ml.shap_explainer import get_shap_explanation
from app.services.redis import *

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictResponse)
async def predict_diabetes(request: PredictRequest):
    try:
        model, scaler, imputer, explainer = get_model_components()
        features = request.to_feature_list()
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]
        explanation = get_shap_explanation(
            features, scaler, imputer, explainer
        )
        return PredictResponse(
            name=request.name,
            prediction="Diabetic" if prediction == 1 else "Not Diabetic",
            probability=round(probability * 100, 2),
            explanation=explanation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
