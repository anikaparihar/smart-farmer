"""
train.py
--------
Trains a Decision Tree classifier and a Random Forest classifier
on the crop recommendation dataset, then saves the best model.
"""

import os
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from preprocess import load_data, encode_labels, split_data


def train_decision_tree(X_train, y_train, max_depth: int = 10):
    """Train a Decision Tree and return the fitted model."""
    dt = DecisionTreeClassifier(
        max_depth=max_depth,
        criterion="gini",
        random_state=42
    )
    dt.fit(X_train, y_train)
    return dt


def train_random_forest(X_train, y_train, n_estimators: int = 100):
    """Train a Random Forest and return the fitted model."""
    rf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    return rf


def save_model(model, label_encoder, path: str = "models/crop_model.pkl"):
    """Persist the trained model + label encoder to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump({"model": model, "label_encoder": label_encoder}, path)
    print(f"Model saved to {path}")


if __name__ == "__main__":
    # ── Load & prepare data ──────────────────────────────────────────
    df = load_data()
    df, le = encode_labels(df)
    X_train, X_test, y_train, y_test = split_data(df)

    # ── Train both models ────────────────────────────────────────────
    print("\nTraining Decision Tree ...")
    dt_model = train_decision_tree(X_train, y_train)
    dt_acc = accuracy_score(y_test, dt_model.predict(X_test))
    print(f"  Decision Tree Accuracy : {dt_acc * 100:.2f}%")

    print("\nTraining Random Forest ...")
    rf_model = train_random_forest(X_train, y_train)
    rf_acc = accuracy_score(y_test, rf_model.predict(X_test))
    print(f"  Random Forest Accuracy : {rf_acc * 100:.2f}%")

    # ── Save the best model ──────────────────────────────────────────
    best_model = rf_model if rf_acc >= dt_acc else dt_model
    best_name  = "Random Forest" if rf_acc >= dt_acc else "Decision Tree"
    print(f"\nBest model: {best_name} ({max(rf_acc, dt_acc)*100:.2f}%)")
    save_model(best_model, le)
