import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# ---------------------------------------------------------
# 1. Load the Dataset
# ---------------------------------------------------------
print(" Loading dataset...")
df = pd.read_csv("ml_model/training_data.csv")

# ---------------------------------------------------------
# 2. Feature Engineering (The Secret Sauce)
# ---------------------------------------------------------
# We must convert raw text strings into numerical values that the math model can understand.
print(" Extracting numerical features from commands...")

# Feature 1: Length of the command (Reverse shells are usually long)
df['cmd_length'] = df['executed_cmd'].apply(len)

# Feature 2: Number of special characters (Attackers use lots of pipes and redirects)
special_chars = ['|', '>', '&', '/', ';', '$']
df['num_special_chars'] = df['executed_cmd'].apply(lambda x: sum(x.count(c) for c in special_chars))

# Feature 3: Is it executing from a suspicious directory? (/tmp or /dev)
df['in_suspicious_dir'] = df['executed_cmd'].apply(lambda x: 1 if '/tmp' in x or '/dev' in x else 0  # nosec B108)

# Feature 4: Does it contain network-related keywords?
network_keywords = ['tcp', 'http', 'wget', 'curl', 'nc ']
df['has_network_keyword'] = df['executed_cmd'].apply(lambda x: 1 if any(k in x for k in network_keywords) else 0)

# The features we will actually feed to the model
features = ['cmd_length', 'num_special_chars', 'in_suspicious_dir', 'has_network_keyword']
X = df[features]

# ---------------------------------------------------------
# 3. Train the Isolation Forest
# ---------------------------------------------------------
print(" Training Isolation Forest model...")

# contamination=0.01 means we expect roughly 1% of the training data to be anomalous (50 / 5050 is ~1%)
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

# We fit the model ONLY on the features. We do NOT give it the 'is_anomaly' label.
# This makes it Unsupervised Learning.
model.fit(X)

# ---------------------------------------------------------
# 4. Evaluate the Model (Did it work?)
# ---------------------------------------------------------
# The model outputs -1 for anomalies and 1 for normal data.
df['predictions'] = model.predict(X)

# Let's map -1 to 1 (anomaly) and 1 to 0 (normal) to match our label format
df['predictions'] = df['predictions'].map({-1: 1, 1: 0})

# Check how many anomalies it caught
correct_anomalies = len(df[(df['is_anomaly'] == 1) & (df['predictions'] == 1)])
total_anomalies = len(df[df['is_anomaly'] == 1])

print(f" Model Evaluation:")
print(f"   Caught {correct_anomalies} out of {total_anomalies} anomalies.")

# ---------------------------------------------------------
# 5. Save the "Brain"
# ---------------------------------------------------------
model_path = "ml_model/isolation_forest.pkl"
joblib.dump(model, model_path)
print(f" Model saved to: {model_path}")
