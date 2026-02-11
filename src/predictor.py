import joblib
import pandas as pd
import os
import sys
from src.extractor import URLExtractor

class URLPredictor:
    def __init__(self, model_path='models/url_model.pkl'):
        # Check if the model exists before trying to load it
        if not os.path.exists(model_path):
            print(f"❌ Error: Model file not found at {model_path}")
            print("Please run 'python train.py' first to train and save the model.")
            sys.exit(1)
        
        # Load the trained model and the feature extractor
        self.model = joblib.load(model_path)
        self.extractor = URLExtractor()
        print("✅ URL Detector Engine Loaded and Ready.")

    def predict(self, url):
        # 1. Extract features from the input URL
        features = self.extractor.extract_features(url)
        
        # 2. Convert to DataFrame (the format the model expects)
        features_df = pd.DataFrame([features])
        
        # 3. Get probability (How sure is the AI?)
        # [Probability of Safe, Probability of Malicious]
        probabilities = self.model.predict_proba(features_df)[0]
        malicious_prob = probabilities[1]
        
        # 4. Get the hard prediction (0 or 1)
        prediction = self.model.predict(features_df)[0]
        
        return {
            'url': url,
            'is_malicious': bool(prediction),
            'confidence': malicious_prob * 100,
            'verdict': "🚨 MALICIOUS" if prediction == 1 else "✅ SAFE"
        }

def main():
    # Initialize the predictor
    predictor = URLPredictor()
    
    print("\n--- URL Security Scanner ---")
    print("Type 'exit' to quit.")
    
    while True:
        target_url = input("\nEnter URL to scan: ").strip()
        
        if target_url.lower() == 'exit':
            break
        
        if not target_url:
            continue
            
        try:
            result = predictor.predict(target_url)
            
            print("-" * 30)
            print(f"URL: {result['url']}")
            print(f"VERDICT: {result['verdict']}")
            print(f"CONFIDENCE: {result['confidence']:.2f}%")
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ An error occurred during scanning: {e}")

if __name__ == "__main__":
    main()