# 🛡️ AI-Powered URL Maliciousness Detector

A high-performance machine learning pipeline designed to detect phishing and malicious URLs. This project specifically tackles the **Extreme Class Imbalance** problem (where safe data outweighs malicious data 500-to-1).

## 🚀 Features
* **Shannon Entropy Analysis:** Detects random character patterns in Domain Generation Algorithms (DGA).
* **Structural DNA:** Analyzes Digit-to-URL ratios, Path Depth, and Special Character frequency.
* **Balanced Ensemble Learning:** Uses `EasyEnsemble` and `BalancedRandomForest` to ensure high recall even with limited threat samples.

## 📊 Model Performance
In training, we achieved a **Recall of 0.88** on the minority class by utilizing advanced resampling techniques.

| Metric | Safe (0) | Malicious (1) |
| :--- | :--- | :--- |
| **Precision** | 1.00 | 0.82 |
| **Recall** | 0.98 | 0.88 |

## 🛠️ Installation & Usage
1. Clone the repo: `git clone https://github.com/aishvibansal/url-detector.git`
2. Install dependencies: `pip install pandas scikit-learn imbalanced-learn joblib`
3. Train the model: `python train.py`
4. Scan a URL: `python predictor.py`