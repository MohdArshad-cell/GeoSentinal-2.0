import pandas as pd
import os
from datetime import datetime

# Import Engines
from engine.gemini_client import GeoSentinalAI
from engine.relevance_filter import RelevanceFilter
from engine.sentiment_analyzer import SentimentAnalyzer

# Import Providers
from providers.acled_provider import ACLEDProvider
from providers.gdelt_provider import GDELTProvider
from providers.news_api_provider import NewsAPIProvider

# Import Processors
from processor.pca_weights import calculate_dynamic_weights
from processor.normalization import GeoNormalization

class GeoSentinalController:
    def __init__(self):
        # Initialize AI Engine (Hybrid Logic: Gemini + DistilBERT)
        self.ai_client = GeoSentinalAI()
        self.relevance_filter = RelevanceFilter(self.ai_client)
        self.sentiment_scorer = SentimentAnalyzer() # DistilBERT
        
        # Initialize Providers
        self.kinetic_provider = ACLEDProvider()
        self.gdelt_provider = GDELTProvider()
        self.news_provider = NewsAPIProvider()
        
        # Initialize Math Processors
        self.normalizer = GeoNormalization()
        self.db_path = "gpti_history.csv"

    def run_daily_pipeline(self, country_a, country_b):
        print(f"--- Launching GeoSentinal Pipeline: {country_a} vs {country_b} ---")

        # 1. Fetch Pillar 1 (MCT - Kinetic ground truth)
        mct_raw = self.kinetic_provider.fetch_kinetic_data(country_a)
        
        # 2. Fetch Pillar 2 (INT - Multi-source Narrative)
        gdelt_data = self.gdelt_provider.fetch_narrative_data(country_a, country_b)
        news_data = self.news_provider.fetch_global_news(country_a, country_b)
        all_narratives = gdelt_data + news_data

        # 3. Hybrid AI Analysis (The "Gatekeeper" + "Scorer")
        valid_scores = []
        for item in all_narratives:
            # Gemini Relevance Filter (The Brain)
            if self.relevance_filter.is_relevant(item['text'], country_a, country_b):
                # DistilBERT Sentiment Analysis (The Speed)
                score = self.sentiment_scorer.get_sentiment_score(item['text'])
                # Geopolitical nuance adjustment
                refined_score = self.sentiment_scorer.apply_geopolitical_logic(item['text'], score)
                valid_scores.append(refined_score)

        # Calculate Raw INT Score
        int_raw = abs(sum(valid_scores) / len(valid_scores)) * len(valid_scores) if valid_scores else 0

        # 4. Data Persistence (DB Simulation for Rolling Window)
        new_entry = pd.DataFrame([{
            "timestamp": datetime.now(),
            "mct_raw": mct_raw,
            "int_raw": int_raw
        }])
        
        if os.path.exists(self.db_path):
            history_df = pd.read_csv(self.db_path)
            history_df = pd.concat([history_df, new_entry], ignore_index=True)
        else:
            history_df = new_entry
        
        history_df.to_csv(self.db_path, index=False)

        # 5. Normalization (36-month rolling Min-Max)
        norm_df = self.normalizer.process_pillars(history_df)
        mct_norm = norm_df['mct_norm'].iloc[-1]
        int_norm = norm_df['int_norm'].iloc[-1]

        # 6. Dynamic PCA Weighting
        # Pura history bhej rahe hain taaki PCA crash na ho
        weights = calculate_dynamic_weights(norm_df['mct_norm'].tolist(), norm_df['int_norm'].tolist())
        
        # 7. Final GPTI Calculation
        final_index = (weights['w_mct'] * mct_norm) + (weights['w_int'] * int_norm)

        print(f"Pillar Weights: MCT={weights['w_mct']:.2f}, INT={weights['w_int']:.2f}")
        print(f"--- Final GPTI Score: {final_index:.2f} ---")

        return {
            "gpti": final_index,
            "mct": mct_norm,
            "int": int_norm,
            "weights": weights
        }

if __name__ == "__main__":
    controller = GeoSentinalController()
    controller.run_daily_pipeline("India", "Pakistan")