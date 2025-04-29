from typing import Dict, List, Optional
import json

class DiagnosisAssistant:
    """
    A simple AI assistant for helping with diagnoses.
    In a real application, this would integrate with a medical AI service.
    """
    
    def __init__(self):
        # Sample knowledge base for demonstration purposes
        self.symptoms_to_conditions = {
            "fever": ["Common Cold", "Flu", "COVID-19", "Pneumonia"],
            "cough": ["Common Cold", "Flu", "COVID-19", "Pneumonia", "Bronchitis"],
            "headache": ["Migraine", "Tension Headache", "Sinusitis", "Flu"],
            "fatigue": ["Anemia", "Depression", "Hypothyroidism", "Flu", "COVID-19"],
            "nausea": ["Food Poisoning", "Migraine", "Gastritis", "Pregnancy"],
            "dizziness": ["Vertigo", "Low Blood Pressure", "Anemia", "Dehydration"],
            "chest pain": ["Angina", "Heart Attack", "Acid Reflux", "Costochondritis"],
            "shortness of breath": ["Asthma", "COPD", "Heart Failure", "Pneumonia", "COVID-19"],
            "abdominal pain": ["Appendicitis", "Gastritis", "IBS", "Kidney Stones", "Pancreatitis"]
        }
        
        self.condition_descriptions = {
            "Common Cold": "A viral infection of the upper respiratory tract. Usually harmless and resolves within 7-10 days.",
            "Flu": "Influenza is a viral infection that attacks your respiratory system. More severe than a common cold.",
            "COVID-19": "A respiratory illness caused by the SARS-CoV-2 virus. Symptoms range from mild to severe.",
            "Pneumonia": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid.",
            "Bronchitis": "Inflammation of the lining of the bronchial tubes, which carry air to and from the lungs.",
            "Migraine": "A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound.",
            "Tension Headache": "A mild to moderate pain often described as feeling like a tight band around the head.",
            "Sinusitis": "Inflammation of the sinuses, usually due to infection or allergies.",
            "Anemia": "A condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues.",
            "Depression": "A mental health disorder characterized by persistently depressed mood or loss of interest in activities.",
            "Hypothyroidism": "A condition in which the thyroid gland doesn't produce enough thyroid hormone.",
            "Food Poisoning": "Illness caused by eating contaminated food. Symptoms include nausea, vomiting, and diarrhea.",
            "Gastritis": "Inflammation of the lining of the stomach, often caused by infection or irritation.",
            "Vertigo": "A sensation of feeling off balance or that you or your surroundings are spinning or moving.",
            "Low Blood Pressure": "A blood pressure reading lower than normal, which can cause dizziness and fainting.",
            "Dehydration": "A condition that occurs when your body loses more fluids than it takes in.",
            "Angina": "Chest pain caused by reduced blood flow to the heart muscle.",
            "Heart Attack": "Occurs when blood flow to a part of the heart is blocked, causing damage to the heart muscle.",
            "Acid Reflux": "A condition where stomach acid flows back into the esophagus, causing irritation.",
            "Costochondritis": "Inflammation of the cartilage that connects a rib to the breastbone.",
            "Asthma": "A condition in which your airways narrow and swell and produce extra mucus.",
            "COPD": "Chronic obstructive pulmonary disease, a chronic inflammatory lung disease that causes obstructed airflow.",
            "Heart Failure": "A chronic condition in which the heart doesn't pump blood as well as it should.",
            "Appendicitis": "Inflammation of the appendix, causing severe abdominal pain.",
            "IBS": "Irritable bowel syndrome, a common disorder that affects the large intestine.",
            "Kidney Stones": "Hard deposits made of minerals and salts that form inside your kidneys.",
            "Pancreatitis": "Inflammation in the pancreas, which can cause severe abdominal pain."
        }
    
    def analyze_symptoms(self, symptoms: List[str]) -> Dict:
        """
        Analyze a list of symptoms and return possible conditions
        """
        if not symptoms:
            return {
                "possible_conditions": [],
                "recommendation": "No symptoms provided. Please provide symptoms for analysis."
            }
        
        # Count occurrences of each condition based on symptoms
        condition_counts = {}
        
        for symptom in symptoms:
            symptom = symptom.lower()
            if symptom in self.symptoms_to_conditions:
                for condition in self.symptoms_to_conditions[symptom]:
                    if condition in condition_counts:
                        condition_counts[condition] += 1
                    else:
                        condition_counts[condition] = 1
        
        # Sort conditions by count (most matching symptoms first)
        sorted_conditions = sorted(condition_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Prepare results
        results = []
        for condition, count in sorted_conditions:
            results.append({
                "condition": condition,
                "matching_symptoms": count,
                "description": self.condition_descriptions.get(condition, "No description available")
            })
        
        # Generate recommendation
        recommendation = "Based on the symptoms provided, these conditions are possible. "
        if results:
            recommendation += f"The most likely condition might be {results[0]['condition']}. "
        recommendation += "Please consult with a healthcare professional for proper diagnosis."
        
        return {
            "possible_conditions": results,
            "recommendation": recommendation
        }
    
    def get_medication_suggestions(self, condition: str) -> Dict:
        """
        Get medication suggestions for a given condition
        """
        # Sample medication suggestions (for demonstration only)
        medication_map = {
            "Common Cold": ["Acetaminophen", "Decongestants", "Cough suppressants"],
            "Flu": ["Oseltamivir (Tamiflu)", "Acetaminophen", "Ibuprofen"],
            "COVID-19": ["Acetaminophen", "Ibuprofen", "Consult doctor for specific treatments"],
            "Pneumonia": ["Antibiotics (if bacterial)", "Cough medicine", "Pain relievers"],
            "Migraine": ["Sumatriptan", "Rizatriptan", "Ibuprofen", "Acetaminophen"],
            "Hypertension": ["ACE inhibitors", "Angiotensin II receptor blockers", "Calcium channel blockers"],
            "Type 2 Diabetes": ["Metformin", "Sulfonylureas", "DPP-4 inhibitors"],
            "Gastritis": ["Proton pump inhibitors", "H2 blockers", "Antacids"]
        }
        
        if condition in medication_map:
            return {
                "condition": condition,
                "medications": medication_map[condition],
                "note": "These are general suggestions. Always consult with a healthcare professional before starting any medication."
            }
        else:
            return {
                "condition": condition,
                "medications": [],
                "note": "No specific medication suggestions available for this condition. Please consult with a healthcare professional."
            }

# Example usage
if __name__ == "__main__":
    assistant = DiagnosisAssistant()
    result = assistant.analyze_symptoms(["fever", "cough", "fatigue"])
    print(json.dumps(result, indent=2))
    
    med_suggestions = assistant.get_medication_suggestions("Flu")
    print(json.dumps(med_suggestions, indent=2))