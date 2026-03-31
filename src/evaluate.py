"""
evaluate.py
-----------
Loads the saved model and evaluates it on the test set.
Prints accuracy, full classification report, and plots
a confusion matrix heatmap.
"""

import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from preprocess import load_data, encode_labels, split_data


def load_model(path: str = "models/crop_model.pkl"):
    """Load the saved model bundle from disk."""
    bundle = joblib.load(path)
    return bundle["model"], bundle["label_encoder"]


def plot_confusion_matrix(cm, class_names):
    """Plot a labelled confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="YlGn",
        xticklabels=class_names,
        yticklabels=class_names,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_xlabel("Predicted Crop", fontsize=12)
    ax.set_ylabel("Actual Crop", fontsize=12)
    ax.set_title("Confusion Matrix — Crop Recommendation", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig("models/confusion_matrix.png", dpi=150)
    plt.show()
    print("Confusion matrix saved to models/confusion_matrix.png")


if __name__ == "__main__":
    # ── Data ─────────────────────────────────────────────────────────
    df = load_data()
    df, le = encode_labels(df)
    _, X_test, _, y_test = split_data(df)

    # ── Model ────────────────────────────────────────────────────────
    model, le_loaded = load_model()

    # ── Predictions ──────────────────────────────────────────────────
    y_pred = model.predict(X_test)

    # ── Metrics ──────────────────────────────────────────────────────
    acc = accuracy_score(y_test, y_pred)
    print(f"\nOverall Accuracy : {acc * 100:.2f}%\n")
    print("=== Classification Report ===")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=le_loaded.classes_,
        )
    )

    # ── Confusion Matrix ─────────────────────────────────────────────
    cm = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(cm, le_loaded.classes_)
