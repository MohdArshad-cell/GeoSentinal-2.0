import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeoSentinalAI:
    def __init__(self):
        # Gemini 1.5 Flash: Choice for high-throughput and complex reasoning [cite: 178, 179]
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def analyze_text(self, text, country_a, country_b):
        """
        Implements the symbiotic AI division of labor: 
        1. Nuanced Relevance Filtering [cite: 173]
        2. Specialized Sentiment Analysis [cite: 156]
        """
        
        # Perfect Prompt based on PDF logic [cite: 183]
        prompt = f"""
        ROLE:
        You are a senior geopolitical analyst specializing in global conflict analysis[cite: 183]. 
        Your task is to determine if the text discusses genuine geopolitical tension between {country_a} and {country_b}.

        STRICT DEFINITIONS & FILTERS:
        - Geopolitical Tension: Military, diplomatic, or political conflicts, threats, or escalations[cite: 183].
        - EXCLUSIONS: Does NOT include sports (e.g. cricket matches), cultural events, celebrities, or routine economic trade[cite: 177, 183].
        
        PILLAR CLASSIFICATION[cite: 58, 59]:
        - 'Kinetic' (MCT): Physical events, military actions, border skirmishes, or violence[cite: 6, 62].
        - 'Narrative' (INT): Verbal threats, escalatory rhetoric, media framing, or diplomatic hostility[cite: 7, 80].

        TASK:
        1. relevant: 'Yes' if it meets the inclusion criteria, 'No' if it is noise or excluded[cite: 183].
        2. score: If relevant, provide a sentiment score from -1.0 (Highly Hostile/Escalatory) to +1.0 (Peaceful/De-escalatory)[cite: 169].
        3. pillar: Classify as 'Kinetic' or 'Narrative'[cite: 59].
        4. reason: A 1-sentence explanation of your decision.

        OUTPUT FORMAT: Strictly valid JSON only.
        Example: {{"relevant": "Yes", "score": -0.85, "pillar": "Narrative", "reason": "Official state threat of sanctions."}}

        TEXT TO ANALYZE:
        "{text}"
        """

        try:
            # LLM as a 'Cognitive Filter' [cite: 154, 188]
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            # Filtering noise: Only keep 'Yes' responses [cite: 185, 186]
            if result.get("relevant") == "Yes":
                return result
            return None
            
        except Exception as e:
            print(f"Error in GeoSentinal AI Engine: {e}")
            return None