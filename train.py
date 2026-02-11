import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imblearn.ensemble import BalancedRandomForestClassifier
from src.extractor import URLExtractor

def train_final_model(csv_path):
    print("--- 🚀 Initializing Extreme Imbalance Training ---")
    df = pd.read_csv(csv_path)
    
    url_col = df.columns[0]
    label_col = df.columns[1]

    extractor = URLExtractor()
    print("Extracting Entropy and Token features...")
    X = pd.DataFrame([extractor.extract_features(str(u)) for u in df[url_col]])
    
    # Map labels: 0=Safe, 1=Malicious
    y = df[label_col].apply(lambda x: 0 if str(x).strip().lower() in ['0', 'benign', 'safe'] else 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    print(f"Dataset Split: {y_train.value_counts().to_dict()}")

    # Using BalancedRandomForest which downsamples the majority class in each bootstrap
    print("Training Balanced Random Forest (Under-sampling Majority)...")
    model = BalancedRandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        sampling_strategy='all',
        replacement=True,
        bootstrap=True,
        n_jobs=-1,
        random_state=42
    )
    
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    print("\n" + "="*40)
    print("      FINAL BALANCED PERFORMANCE")
    print("="*40)
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Malicious']))

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/url_model.pkl')
    print(f"\n✅ Model saved to models/url_model.pkl")

if __name__ == "__main__":
    train_final_model('data/malicious_phish.csv')