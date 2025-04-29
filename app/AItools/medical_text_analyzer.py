from typing import Dict, List, Optional
import re

class MedicalTextAnalyzer:
    """
    A simple medical text analyzer for extracting medical information from text.
    In a real application, this would use NLP models for more accurate analysis.
    """
    
    def __init__(self):
        # Sample medical terms for demonstration
        self.medical_terms = {
            "symptoms": [
                "fever", "cough", "headache", "nausea", "vomiting", "dizziness", 
                "fatigue", "pain", "rash", "swelling", "shortness of breath",
                "chest pain", "abdominal pain", "back pain"
            ],
            "conditions": [
                "diabetes", "hypertension", "asthma", "arthritis", "depression",
                "anxiety", "cancer", "heart disease", "stroke", "pneumonia",
                "influenza", "covid", "migraine", "allergy"
            ],
            "medications": [
                "aspirin", "ibuprofen", "acetaminophen", "paracetamol", "metformin",
                "insulin", "lisinopril", "atorvastatin", "amoxicillin", "omeprazole",
                "albuterol", "fluoxetine", "warfarin", "prednisone"
            ],
            "procedures": [
                "surgery", "x-ray", "mri", "ct scan", "ultrasound", "biopsy",
                "blood test", "vaccination", "immunization", "physical therapy"
            ]
        }
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze medical text and extract relevant information
        """
        if not text:
            return {
                "extracted_info": {},
                "summary": "No text provided for analysis."
            }
        
        text = text.lower()
        
        # Extract information
        extracted_info = {
            "symptoms": self._extract_terms(text, self.medical_terms["symptoms"]),
            "conditions": self._extract_terms(text, self.medical_terms["conditions"]),
            "medications": self._extract_terms(text, self.medical_terms["medications"]),
            "procedures": self._extract_terms(text, self.medical_terms["procedures"])
        }
        
        # Generate summary
        summary = self._generate_summary(extracted_info)
        
        return {
            "extracted_info": extracted_info,
            "summary": summary
        }
    
    def _extract_terms(self, text: str, term_list: List[str]) -> List[str]:
        """
        Extract terms from text based on a list of terms
        """
        found_terms = []
        
        for term in term_list:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, text):
                found_terms.append(term)
        
        return found_terms
    
    def _generate_summary(self, extracted_info: Dict) -> str:
        """
        Generate a summary based on extracted information
        """
        summary_parts = []
        
        if extracted_info["symptoms"]:
            symptoms_str = ", ".join(extracted_info["symptoms"])
            summary_parts.append(f"Symptoms mentioned: {symptoms_str}.")
        
        if extracted_info["conditions"]:
            conditions_str = ", ".join(extracted_info["conditions"])
            summary_parts.append(f"Medical conditions mentioned: {conditions_str}.")
        
        if extracted_info["medications"]:
            medications_str = ", ".join(extracted_info["medications"])
            summary_parts.append(f"Medications mentioned: {medications_str}.")
        
        if extracted_info["procedures"]:
            procedures_str = ", ".join(extracted_info["procedures"])
            summary_parts.append(f"Medical procedures mentioned: {procedures_str}.")
        
        if not summary_parts:
            return "No relevant medical information found in the text."
        
        return " ".join(summary_parts)
    
    def generate_structured_notes(self, text: str) -> Dict:
        """
        Generate structured medical notes from free text
        """
        analysis = self.analyze_text(text)
        
        # Create SOAP note structure
        # (Subjective, Objective, Assessment, Plan)
        soap_note = {
            "subjective": "",
            "objective": "",
            "assessment": "",
            "plan": ""
        }
        
        # Extract sentences that might contain subjective information
        subjective_patterns = [
            r'(?i)patient.{1,50}(reports|complains|states|mentions|describes)',
            r'(?i)(reports|complains|states|mentions|describes).{1,50}(pain|discomfort|feeling)'
        ]
        
        for pattern in subjective_patterns:
            matches = re.findall(pattern, text)
            if matches:
                soap_note["subjective"] += " ".join([m[0] if isinstance(m, tuple) else m for m in matches])
        
        # Extract sentences that might contain objective information
        objective_patterns = [
            r'(?i)(examination|exam|vital signs|temperature|pulse|blood pressure).{1,100}',
            r'(?i)(observed|measured|found|noted).{1,100}'
        ]
        
        for pattern in objective_patterns:
            matches = re.findall(pattern, text)
            if matches:
                soap_note["objective"] += " ".join([m[0] if isinstance(m, tuple) else m for m in matches])
        
        # Use conditions as assessment
        if analysis["extracted_info"]["conditions"]:
            soap_note["assessment"] = "Possible conditions: " + ", ".join(analysis["extracted_info"]["conditions"])
        
        # Use medications and procedures as plan
        plan_parts = []
        if analysis["extracted_info"]["medications"]:
            plan_parts.append("Medications: " + ", ".join(analysis["extracted_info"]["medications"]))
        
        if analysis["extracted_info"]["procedures"]:
            plan_parts.append("Procedures: " + ", ".join(analysis["extracted_info"]["procedures"]))
        
        soap_note["plan"] = " ".join(plan_parts)
        
        # Fill in defaults for empty sections
        for key in soap_note:
            if not soap_note[key]:
                soap_note[key] = f"No {key} information extracted."
        
        return {
            "soap_note": soap_note,
            "extracted_terms": analysis["extracted_info"]
        }

# Example usage
if __name__ == "__main__":
    analyzer = MedicalTextAnalyzer()
    
    sample_text = """
    Patient reports severe headache and fever for the past 3 days. 
    Also complains of cough and fatigue. Has been taking ibuprofen for pain.
    Patient has a history of asthma and uses albuterol inhaler as needed.
    Recommended a chest x-ray to rule out pneumonia.
    """
    
    result = analyzer.analyze_text(sample_text)
    print(result["summary"])
    
    structured_notes = analyzer.generate_structured_notes(sample_text)
    for section, content in structured_notes["soap_note"].items():
        print(f"{section.upper()}: {content}")