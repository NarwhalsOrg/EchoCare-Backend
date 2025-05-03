import joblib
import shap
import numpy as np
import os

# Paths to your artifacts (adjust if needed)
ARTIFACT_DIR = os.path.dirname(__file__) + "/artifacts/"
MODEL_PATH = ARTIFACT_DIR + "linear_svm_model.pkl"
SCALER_PATH = ARTIFACT_DIR + "scaler.pkl"
XTRAIN_SAMPLE_PATH = ARTIFACT_DIR + "X_train_sample.pkl"

# Load model, scaler, and sample training data for SHAP
linear_svm_model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
X_train_sample = joblib.load(XTRAIN_SAMPLE_PATH)

# Feature names in the correct order (excluding ID)
FEATURE_NAMES = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", "HeartDiseaseorAttack",
    "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost",
    "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"
]

def predict_and_explain(patient_data: dict):
    """
    Predict diabetes and provide SHAP explanations for a single patient.
    patient_data: dict with all 21 features (excluding ID)
    Returns: dict with prediction, probability, label, and explanations
    """
    # Prepare features in the correct order
    patient_features = [patient_data[name] for name in FEATURE_NAMES]
    patient_scaled = scaler.transform([patient_features])

    # Prediction (0 = not diabetic, 1 = diabetic)
    prediction = int(linear_svm_model.predict(patient_scaled)[0])

    # Probability (use sigmoid on decision_function if not calibrated)
    try:
        proba = float(linear_svm_model.predict_proba(patient_scaled)[0][1])
    except AttributeError:
        from scipy.special import expit
        decision = linear_svm_model.decision_function(patient_scaled)[0]
        proba = float(expit(decision))

    # SHAP explanation
    explainer = shap.KernelExplainer(
        linear_svm_model.predict,
        scaler.transform(X_train_sample.sample(100, random_state=42))
    )
    shap_values = explainer.shap_values(patient_scaled)[0]
    feature_impacts = list(zip(FEATURE_NAMES, shap_values))
    feature_impacts_sorted = sorted(feature_impacts, key=lambda x: abs(x[1]), reverse=True)

    explanations = []
    for feature, impact in feature_impacts_sorted:
        if impact > 0:
            explanations.append(f"The feature **{feature}** pushes towards the patient being diabetic (+{impact:.2f}).")
        else:
            explanations.append(f"The feature **{feature}** pushes towards the patient NOT being diabetic ({impact:.2f}).")

    # Human-friendly label
    prediction_label = (
        f"⚠️ The patient is likely diabetic ({proba*100:.0f}% probability)."
        if prediction == 1 else
        f"✅ The patient is likely not diabetic ({(1-proba)*100:.0f}% probability)."
    )

    return {
        "prediction": prediction,
        "probability": round(proba, 2),
        "probability_percent": f"{proba*100:.0f}%",
        "prediction_label": prediction_label,
        "explanations": explanations
    }
