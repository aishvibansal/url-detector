import requests
import base64
import os
import time
from dotenv import load_dotenv

load_dotenv()

class VirusTotalClient:
    def __init__(self):
        self.api_key = os.getenv("VT_API_KEY")
        self.base_url = "https://www.virustotal.com/api/v3/urls"

    def get_report(self, url):
        """Fetch report from VT. Returns 404 if the URL hasn't been scanned yet."""
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        headers = {"x-apikey": self.api_key, "accept": "application/json"}
        
        response = requests.get(f"{self.base_url}/{url_id}", headers=headers)
        return response

    def submit_url(self, url):
        """Submit a new URL to VT for analysis."""
        headers = {"x-apikey": self.api_key}
        response = requests.post(self.base_url, headers=headers, data={"url": url})
        return response.status_code == 200

    def check_url_robust(self, url):
        """Logic to get a report or submit if it's missing."""
        if not self.api_key:
            return {"error": "API Key missing in .env"}

        response = self.get_report(url)
        
        if response.status_code == 404:
            print("URL not in database. Submitting for scan...")
            if self.submit_url(url):
                time.sleep(15) # Wait for VT to process
                response = self.get_report(url)
            else:
                return {"error": "Could not submit URL to VT"}

        if response.status_code == 200:
            stats = response.json()['data']['attributes']['last_analysis_stats']
            return {
                "malicious": stats['malicious'],
                "suspicious": stats['suspicious'],
                "verdict": "MALICIOUS" if stats['malicious'] > 0 else "CLEAN"
            }
        
        return {"error": f"API Error: {response.status_code}"}