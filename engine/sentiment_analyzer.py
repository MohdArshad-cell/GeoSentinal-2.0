from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

class SentimentAnalyzer:
    def __init__(self):
        """
        PDF Section 4.2: Fine-tuned DistilBERT model for high-throughput 
        geopolitical sentiment analysis.
        """
        # Model: DistilBERT (97% language capability of BERT with fraction of cost)
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def get_sentiment_score(self, text):
        """
        Processes text to return a score from -1.0 to +1.0.
        High-throughput stage: Optimized for thousands of documents per minute.
        """
        # Tokenize input text
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Softmax to get probabilities
            probs = F.softmax(outputs.logits, dim=-1)
            
        # DistilBERT logic: Map Negative/Positive labels to -1.0/+1.0 range
        # Probability of Positive (index 1) - Probability of Negative (index 0)
        neg_prob = probs[0][0].item()
        pos_prob = probs[0][1].item()
        
        final_score = pos_prob - neg_prob
        return round(final_score, 4)

    def apply_geopolitical_logic(self, text, base_score):
        """
        PDF Section 4.2: Lexicon of geopolitics is specialized.
        'Successful' military tests must be treated as Negative (Tension).
        """
        # PDF Example: "successful missile test" is negative for bilateral tension
        hostile_indicators = ['missile', 'nuclear', 'airstrike', 'drills', 'troop deployment']
        
        text_lower = text.lower()
        if any(word in text_lower for word in hostile_indicators):
            # Agar 'success' word hai military context mein, score ko negative force karo
            if "success" in text_lower or "achieved" in text_lower:
                return -0.85 # Forced negative for tension index
        
        return base_score