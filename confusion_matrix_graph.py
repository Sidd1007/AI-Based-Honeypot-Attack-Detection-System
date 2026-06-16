import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay

# Load dataset
data = pd.read_csv("honeypot_features.csv")

data['attack_label'] = (
    data['attack_label']
    .astype(str)
    .str.strip()
    .str.lower()
)

data['attack_label'] = data['attack_label'].map({
    'interactive': 0,
    'brute_force': 1
})

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

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

ConfusionMatrixDisplay.from_estimator(
    model,
    X_test,
    y_test,
    display_labels=[
        "Interactive",
        "Brute Force"
    ]
)

plt.title("Confusion Matrix")
plt.tight_layout()

plt.savefig("confusion_matrix.png")
plt.show()
