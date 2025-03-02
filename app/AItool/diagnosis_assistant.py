from typing import List, Dict, Any, Optional
import json

class DiagnosisAssistant:
    """
    AI-powered diagnosis assistant that provides suggestions based on symptoms.
    This is a placeholder implementation that would be connected to an actual AI model.
    """
    
    def __init__(self):
        self.symptoms_db = self._load_symptoms_db()
        
    def _load_symptoms_db(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load the symptoms database from the demo data"""
        try:
            with open("app/demoData/symptoms.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty database if file doesn't exist or is invalid
            return {}
            
    async def analyze_symptoms(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        Analyze symptoms and provide possible diagnoses
        
        Args:
            symptoms: List of symptoms reported by the patient
            
        Returns:
            Dictionary containing possible diagnoses and recommendations
        """
        possible_conditions = []
        
        # Simple matching algorithm (would be replaced by ML model)
        for symptom in symptoms:
            if symptom in self.symptoms_db:
                for condition in self.symptoms_db[symptom]:
                    if condition not in possible_conditions:
                        possible_conditions.append(condition)
        
        # Sort by confidence score
        possible_conditions.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        
        return {
            "possible_diagnoses": possible_conditions[:3],  # Top 3 matches
            "recommendation": self._generate_recommendation(possible_conditions),
            "disclaimer": "This is an AI-assisted suggestion and not a medical diagnosis. Please consult with a healthcare professional."
        }
        
    def _generate_recommendation(self, conditions: List[Dict[str, Any]]) -> str:
        """Generate a recommendation based on possible conditions"""
        if not conditions:
            return "No matching conditions found. Please consult with a healthcare professional for proper diagnosis."
            
        severity = max([c.get("severity", 1) for c in conditions])
        
        if severity >= 8:
            return "Urgent medical attention recommended. Please seek immediate medical care."
        elif severity >= 5:
            return "Medical consultation recommended within 24-48 hours."
        else:
            return "Monitor symptoms and schedule a routine appointment if symptoms persist."
            
    async def suggest_tests(self, symptoms: List[str], patient_age: int, patient_gender: str) -> List[str]:
        """
        Suggest medical tests based on symptoms and patient information
        
        Args:
            symptoms: List of symptoms reported by the patient
            patient_age: Age of the patient
            patient_gender: Gender of the patient
            
        Returns:
            List of recommended tests
        """
        # This would be connected to an actual AI model
        # Simple implementation for demonstration
        recommended_tests = []
        
        if "fever" in symptoms or "chills" in symptoms:
            recommended_tests.append("Complete Blood Count (CBC)")
            
        if "chest pain" in symptoms or "shortness of breath" in symptoms:
            recommended_tests.append("ECG/EKG")
            recommended_tests.append("Chest X-ray")
            
        if "headache" in symptoms and "vision changes" in symptoms:
            recommended_tests.append("CT Scan")
            
        if patient_age > 50 and patient_gender.lower() == "male" and "urinary problems" in symptoms:
            recommended_tests.append("PSA Test")
            
        if patient_age > 40 and "fatigue" in symptoms and "weight loss" in symptoms:
            recommended_tests.append("Comprehensive Metabolic Panel")
            recommended_tests.append("Thyroid Function Tests")
            
        # Add general tests if no specific tests were recommended
        if not recommended_tests:
            recommended_tests = ["Complete Blood Count (CBC)", "Basic Metabolic Panel"]
            
        return recommended_tests