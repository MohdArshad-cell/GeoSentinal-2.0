import requests
import pandas as pd

class GDELTProvider:
    def __init__(self):
        # GDELT 2.0 Doc API endpoint for news searching 
        self.base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

    def fetch_narrative_data(self, country_a, country_b, max_results=50):
        """
        Pillar 2 (INT) ke liye global news articles fetch karna[cite: 81, 118].
        """
        print(f"Searching global news for: {country_a} AND {country_b}...")
        
        # Query construction based on PDF keywords [cite: 120, 140]
        query = f'("{country_a}" AND "{country_b}") (military OR conflict OR threat OR diplomatic)'
        
        params = {
            "query": query,
            "mode": "artlist", # Articles ki list mang rahe hain [cite: 140]
            "format": "json",
            "maxrecords": max_results,
            "timespan": "24h" # Sirf pichle 24 ghante ka live data [cite: 119]
        }

        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                # Hum sirf headlines aur snippets nikal rahe hain AI analysis ke liye [cite: 144]
                cleaned_data = []
                for art in articles:
                    cleaned_data.append({
                        "title": art.get('title'),
                        "url": art.get('url'),
                        "source": art.get('sourcecountry'),
                        "text": art.get('title') # Title ko as text pass karenge relevance check ke liye [cite: 190]
                    })
                return cleaned_data
            else:
                print(f"GDELT Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Connection failed to GDELT: {e}")
            return []