import os
import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
import shap

MODEL_PATH = os.path.join("data", "final_model.pkl")
SCALER_PATH = os.path.join("data", "scaler.pkl")
SHAP_DATA_PATH = os.path.join("data", "x_shap.csv")




_model = None
_scaler = None
_imputer = None
_explainer = None

def get_model_components():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"Scaler file not found at {SCALER_PATH}")
    if not os.path.exists(SHAP_DATA_PATH):
        raise FileNotFoundError(f"SHAP data file not found at {SHAP_DATA_PATH}")

    global _model, _scaler, _imputer, _explainer
    if _model is None or _scaler is None or _imputer is None or _explainer is None:
        # Load model and scaler
        _model = joblib.load(MODEL_PATH)
        _scaler = joblib.load(SCALER_PATH)
        # Load SHAP background data
        x_shap = pd.read_csv(SHAP_DATA_PATH)
        _imputer = SimpleImputer(strategy='mean')
        x_shap_imputed = _imputer.fit_transform(x_shap)
        x_scaled = _scaler.fit_transform(x_shap_imputed)
        background = x_scaled[:100]
        _explainer = shap.KernelExplainer(_model.decision_function, background)
    return _model, _scaler, _imputer, _explainer
