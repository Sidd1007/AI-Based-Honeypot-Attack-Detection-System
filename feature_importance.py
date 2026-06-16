import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("honeypot_features.csv")

# Clean labels
data['attack_label'] = (
    data['attack_label']
    .astype(str)
    .str.strip()
    .str.lower()
)

# Convert labels
data['attack_label'] = data['attack_label'].map({
    'interactive': 0,
    'brute_force': 1
})

# Features
feature_cols = [
    'total_attempts',
    'unique_usernames',
    'failed_attempts',
    'success_attempts',
    'avg_time_gap',
    'command_count',
    'session_duration'
]

X = data[feature_cols]
y = data['attack_label']

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X, y)

# Feature importance
importance = model.feature_importances_

# Plot
plt.figure(figsize=(8, 5))
plt.bar(feature_cols, importance)
plt.xticks(rotation=45)
plt.ylabel("Importance Score")
plt.title("Feature Importance in Attack Detection")
plt.tight_layout()

plt.savefig("feature_importance.png")
plt.show()

print("Graph saved as feature_importance.png")
