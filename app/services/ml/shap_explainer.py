def get_shap_explanation(patient_features, scaler, imputer, explainer):
    feature_names = [
        "HighBP", "HighChol", "HeartDiseaseorAttack", "Stroke", "Smoker",
        "PhysActivity", "DiffWalk", "BMI", "MentHlth", "PhysHlth",
        "GenHlth", "Sex", "Age", "HvyAlcoholConsump"
    ]
    imputed = imputer.transform([patient_features])
    scaled = scaler.transform(imputed)
    shap_values = explainer.shap_values(scaled)[0]
    impacts = list(zip(feature_names, shap_values))
    sorted_impacts = sorted(impacts, key=lambda x: abs(x[1]), reverse=True)
    explanations = []
    for feature, impact in sorted_impacts[:5]:  # Top 5 features
        if impact > 0:
            explanations.append(f"The feature **{feature}** increases diabetes risk (+{impact:.2f}).")
        else:
            explanations.append(f"The feature **{feature}** reduces diabetes risk ({impact:.2f}).")
    return explanations
