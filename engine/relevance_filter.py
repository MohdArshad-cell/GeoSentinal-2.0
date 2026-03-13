import json

class RelevanceFilter:
    def __init__(self, ai_client):
        self.ai_client = ai_client

    def get_structured_analysis(self, text, country_a, country_b):
        """
        Geopolitical Tension Index (GPTI) ke liye high-fidelity filtering[cite: 45].
        """
        prompt = f"""
        ROLE:
        You are a Senior Intelligence Analyst specializing in Global Conflict Dynamics. 
        Your task is to classify data for the 'GeoSentinal' Geopolitical Tension Index[cite: 45].

        CONTEXT:
        Analyzing the relationship between {country_a} and {country_b}.

        STRICT INCLUSION CRITERIA (Mark 'Yes'):
        - Military & Conflict (MCT): Border skirmishes, troop movements, missile tests, or kinetic violence[cite: 40, 70, 73].
        - Intelligent Narrative (INT): Escalatory rhetoric, official government threats, diplomatic sanctions, or hostile media framing[cite: 41, 83].

        STRICT EXCLUSION CRITERIA (Mark 'No'):
        - Sports & Culture: Cricket matches, movies, awards, or celebrity news.
        - Routine Economy: Standard trade agreements or business-as-usual economic news.
        - Historical/Archival: Documentaries or old news not triggering current crises.

        FEW-SHOT EXAMPLES:
        - "India defeats Pakistan in World Cup": {{"relevant": "No", "reason": "Sports noise"}}.
        - "Pakistan Foreign Ministry warns of retaliation": {{"relevant": "Yes", "pillar": "Narrative", "score": -0.8}}[cite: 169, 183].
        - "Troops exchange fire at the Line of Control": {{"relevant": "Yes", "pillar": "Kinetic", "score": -1.0}}[cite: 70, 73].

        TASK:
        1. Is this text relevant to genuine state-level tension? ('Yes'/'No') .
        2. Pillar: If 'Yes', is it 'Kinetic' (MCT) or 'Narrative' (INT)?[cite: 59].
        3. Sentiment Score: Provide a score from -1.0 (Highly Escalatory) to +1.0 (De-escalatory)[cite: 157, 169].
        4. Reasoning: Brief justification.

        OUTPUT FORMAT: Strictly valid JSON only.
        TEXT: "{text}"
        """
        
        try:
            # Gemini 1.5 Flash implementation for high-throughput classification [cite: 151, 158]
            response = self.ai_client.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Filter Error: {e}")
            return None