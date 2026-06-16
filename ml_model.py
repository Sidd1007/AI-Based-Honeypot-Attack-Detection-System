import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import cross_val_score

# -----------------------------
# LOAD DATASET
# -----------------------------

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

# Remove rows with labels not mapped
data = data.dropna()

# -----------------------------
# FEATURES
# -----------------------------

feature_cols = [
    'total_attempts',
    'unique_usernames',
    'failed_attempts',
    'success_attempts',
    'avg_time_gap',
    'command_count',
    'session_duration'
]

# Convert features to numeric
for col in feature_cols:
    data[col] = pd.to_numeric(
        data[col],
        errors='coerce'
    )

data = data.dropna()

# -----------------------------
# DATASET INFO
# -----------------------------

print("Dataset Shape:", data.shape)

print("\nLabel Distribution:")
print(data['attack_label'].value_counts())

# -----------------------------
# SPLIT DATA
# -----------------------------

X = data[feature_cols]
y = data['attack_label']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# MODEL
# -----------------------------

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# -----------------------------
# EVALUATION
# -----------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    "\nModel Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)

# -----------------------------
# CROSS VALIDATION
# -----------------------------

scores = cross_val_score(
    model,
    X,
    y,
    cv=3
)

print(
    "\nCross Validation Scores:",
    scores
)

print(
    "Average CV Accuracy: {:.2f}%".format(
        scores.mean() * 100
    )
)

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------

print("\nFeature Importance:")

for feature, importance in zip(
    feature_cols,
    model.feature_importances_
):
    print(
        f"{feature}: {importance:.4f}"
    )
