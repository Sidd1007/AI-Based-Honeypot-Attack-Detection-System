import pandas as pd
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

# Train model
X = data[feature_cols]
y = data['attack_label']

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X, y)

print("\n=== Attack Prediction System ===")

total_attempts = int(input("Total Attempts: "))
unique_usernames = int(input("Unique Usernames: "))
failed_attempts = int(input("Failed Attempts: "))
success_attempts = int(input("Success Attempts: "))
avg_time_gap = float(input("Average Time Gap: "))
command_count = int(input("Command Count: "))
session_duration = float(input("Session Duration: "))

sample = pd.DataFrame([{
    "total_attempts": total_attempts,
    "unique_usernames": unique_usernames,
    "failed_attempts": failed_attempts,
    "success_attempts": success_attempts,
    "avg_time_gap": avg_time_gap,
    "command_count": command_count,
    "session_duration": session_duration
}])

prediction = model.predict(sample)[0]

if prediction == 1:
    print("\nPredicted Attack Type: BRUTE FORCE")
else:
    print("\nPredicted Attack Type: INTERACTIVE")
