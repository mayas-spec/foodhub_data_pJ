from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib
import json
import sys
import os

sys.path.append(os.path.dirname(__file__))
from data_cleaning import fetch_and_clean


def train():
    df = fetch_and_clean()

    df = df[df['is_rated'] == 1].copy()
    df = df.dropna(subset=['rating'])

    cuisine_map = {c: i for i, c in enumerate(sorted(df['cuisine_type'].unique()))}
    df['cuisine_encoded'] = df['cuisine_type'].map(cuisine_map)
    df['cost_bucket_encoded'] = df['cost_bucket'].map({'Low': 0, 'Medium': 1, 'High': 2})

    features = [
        'cost_of_the_order', 'food_preparation_time',
        'delivery_time', 'total_time', 'is_weekend',
        'cuisine_encoded', 'cost_bucket_encoded'
    ]

    X = df[features]
    y = (df['rating'] >= 4).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print(classification_report(y_test, model.predict(X_test)))

    outputs_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)

    _, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_estimator(
        model, X_test, y_test,
        display_labels=['Low (<4)', 'Good (≥4)'],
        ax=ax
    )
    ax.set_title('Random Forest — Confusion Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, 'confusion_matrix.png'), dpi=150)
    plt.show()

    joblib.dump(model, os.path.join(outputs_dir, 'model.pkl'))
    with open(os.path.join(outputs_dir, 'cuisine_encoding.json'), 'w') as f:
        json.dump(cuisine_map, f, indent=2)
    print("Model saved to outputs/model.pkl")
    print("Cuisine encoding saved to outputs/cuisine_encoding.json")


if __name__ == "__main__":
    train()
