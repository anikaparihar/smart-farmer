"""
preprocess.py
-------------
Loads the crop recommendation dataset, inspects it,
and splits it into train/test sets ready for modeling.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def load_data(filepath: str = "data/crop_recommendation.csv"):
    """Load dataset and return a cleaned DataFrame."""
    df = pd.read_csv(filepath)

    # Standardise column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Rename 'label' to 'crop' if needed
    if "label" in df.columns:
        df.rename(columns={"label": "crop"}, inplace=True)

    print("=== Dataset Overview ===")
    print(f"Shape        : {df.shape}")
    print(f"Columns      : {list(df.columns)}")
    print(f"Crops        : {sorted(df['crop'].unique())}")
    print(f"Missing vals : {df.isnull().sum().sum()}")
    print(df.describe().round(2))
    return df


def encode_labels(df: pd.DataFrame):
    """
    Encode the crop name (string) to an integer label.
    Returns the encoded DataFrame and the fitted LabelEncoder.
    """
    le = LabelEncoder()
    df = df.copy()
    df["crop_encoded"] = le.fit_transform(df["crop"])
    return df, le


def split_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Split into features (X) and target (y), then train/test split.
    Features: N, P, K, ph
    Target  : crop_encoded
    """
    feature_cols = ["n", "p", "k", "ph"]
    X = df[feature_cols]
    y = df["crop_encoded"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"\nTrain size : {X_train.shape[0]} samples")
    print(f"Test size  : {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    df = load_data()
    df, le = encode_labels(df)
    X_train, X_test, y_train, y_test = split_data(df)
    print("\nPreprocessing complete.")
