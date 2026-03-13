import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NewsAPIProvider:
    def __init__(self):
        # NewsAPI key setup (.env file mein add karna)
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_global_news(self, country_a, country_b):
        """
        Commercial news aggregation service se targeted articles fetch karna.
        Target: Last 24 hours of geopolitical discourse.
        """
        if not self.api_key:
            print("Error: NEWS_API_KEY missing in .env")
            return []

        # PDF suggested keywords logic
        query = f'("{country_a}" AND "{country_b}") AND (military OR "border conflict" OR diplomat OR threat)'
        
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 50, # Free tier limit around 100
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                
                # Standardized format for the AI Controller
                cleaned_articles = []
                for art in articles:
                    cleaned_articles.append({
                        "title": art.get('title'),
                        "source": art.get('source', {}).get('name'),
                        "text": f"{art.get('title')}. {art.get('description')}", # Context for AI
                        "url": art.get('url')
                    })
                return cleaned_articles
            else:
                print(f"NewsAPI Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Failed to fetch from NewsAPI: {e}")
            return []