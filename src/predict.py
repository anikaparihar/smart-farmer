"""
predict.py
----------
Interactive CLI tool.
Enter soil values and get a crop recommendation instantly.
"""

import joblib
import numpy as np


def load_model(path: str = "models/crop_model.pkl"):
    bundle = joblib.load(path)
    return bundle["model"], bundle["label_encoder"]


def predict_crop(model, le, N: float, P: float, K: float, ph: float) -> str:
    """Return the recommended crop name for given soil parameters."""
    features = np.array([[N, P, K, ph]])
    encoded   = model.predict(features)[0]
    crop_name = le.inverse_transform([encoded])[0]
    return crop_name.capitalize()


def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠  Please enter a valid number.")


if __name__ == "__main__":
    print("=" * 45)
    print("       Smart Farmer — Crop Recommender")
    print("=" * 45)
    print("Enter your soil test results below.\n")

    N  = get_float("Nitrogen   (N)  value : ")
    P  = get_float("Phosphorus (P)  value : ")
    K  = get_float("Potassium  (K)  value : ")
    ph = get_float("pH              value : ")

    model, le = load_model()
    crop = predict_crop(model, le, N, P, K, ph)

    print("\n" + "=" * 45)
    print(f"  Recommended Crop  →  {crop}")
    print("=" * 45)
