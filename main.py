import joblib
import pandas as pd
from src.extractor import URLExtractor

def predict_url(url):
    extractor = URLExtractor()
    model = joblib.load('models/url_model.pkl')
    
    feats = pd.DataFrame([extractor.extract_features(url)])
    # We use predict_proba to get a "Risk Score"
    risk_score = model.predict_proba(feats)[0][1] 
    
    print(f"\nTarget: {url}")
    print(f"Malicious Risk Score: {risk_score * 100:.1f}%")
    
    if risk_score > 0.8:
        print("🛑 STATUS: HIGH RISK - Malicious URL")
    elif risk_score > 0.4:
        print("⚠️ STATUS: SUSPICIOUS - Proceed with caution")
    else:
        print("✅ STATUS: SAFE - No threats detected")

if __name__ == "__main__":
    url = input("Enter URL to scan: ")
    predict_url(url)