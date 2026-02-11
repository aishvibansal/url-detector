import pandas as pd
df = pd.read_csv('data/malicious_phish.csv')
print("--- Column Names ---")
print(df.columns.tolist())
print("\n--- First 5 Rows ---")
print(df.head())
print("\n--- Unique Labels in the Label Column ---")
# Replace 'label' with whatever your label column is named
label_col = df.columns[1] 
print(df[label_col].value_counts())