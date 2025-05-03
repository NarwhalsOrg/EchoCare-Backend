from typing import List, Dict

# List of all required patient fields (excluding ID)
PATIENT_FEATURES = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", "HeartDiseaseorAttack",
    "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost",
    "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"
]

def get_missing_fields(patient_data: Dict) -> List[str]:
    """
    Returns a list of required fields that are missing (None) in patient_data.
    """
    return [field for field in PATIENT_FEATURES if patient_data.get(field) is None]

def is_patient_data_complete(patient_data: Dict) -> bool:
    """
    Returns True if all required fields are present (not None).
    """
    return len(get_missing_fields(patient_data)) == 0

def clean_patient_data(patient_data: Dict) -> Dict:
    """
    Optionally clean or convert patient data (e.g., ensure ints, handle empty strings).
    """
    cleaned = {}
    for k, v in patient_data.items():
        if v == "" or v is None:
            cleaned[k] = None
        elif k in PATIENT_FEATURES:
            # Convert to int or float as appropriate
            try:
                cleaned[k] = float(v) if k == "BMI" else int(v)
            except Exception:
                cleaned[k] = None
        else:
            cleaned[k] = v
    return cleaned
