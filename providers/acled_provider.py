import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class ACLEDProvider:
    def __init__(self):
        self.email = os.getenv("ACLED_EMAIL")
        self.password = os.getenv("ACLED_PASSWORD")
        self.token_url = "https://acleddata.com/oauth/token"
        self.api_url = "https://acleddata.com/api/acled/read"
        self.access_token = None

    def get_token(self):
        """Documentation ke 'OAuth method' ke hisab se token lena."""
        data = {
            'username': self.email,
            'password': self.password,
            'grant_type': 'password',
            'client_id': 'acled'
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            return self.access_token
        else:
            print("Token Error:", response.text)
            return None

    def fetch_kinetic_data(self, country):
        """Actual kinetic events (MCT Pillar) fetch karna[cite: 66]."""
        if not self.access_token:
            self.get_token()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        # PDF logic: Battles aur Explosions ko filter karna [cite: 70, 73]
        params = {
            'country': country,
            'limit': 100,
            'event_type': 'Battles:OR:event_type=Explosions/Remote violence',
            '_format': 'json'
        }
        
        response = requests.get(self.api_url, headers=headers, params=params)
        if response.status_code == 200:
            events = response.json().get('data', [])
            return self.process_severity(events)
        return []

    def process_severity(self, events):
        """PDF ke 'Event Severity Weighting' rubric ko apply karna[cite: 71, 72]."""
        weighted_score = 0
        for event in events:
            # Battles receive higher weight than others [cite: 73]
            if event['event_type'] == 'Battles':
                weighted_score += 10
            elif event['event_type'] == 'Explosions/Remote violence':
                weighted_score += 7
            else:
                weighted_score += 1
        return weighted_score