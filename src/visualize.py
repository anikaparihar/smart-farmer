"""
visualize.py
------------
Generates exploratory and model-interpretation visualisations:
  1. Pairplot  — joint distributions of N, P, K, pH coloured by crop
  2. Correlation heatmap of all features
  3. Feature importance bar chart (from the trained model)
  4. Decision Tree structure (exported as PNG)
"""

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, export_graphviz, plot_tree

from preprocess import load_data, encode_labels


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_model(path: str = "models/crop_model.pkl"):
    bundle = joblib.load(path)
    return bundle["model"], bundle["label_encoder"]


# ── 1. Pairplot (Joint Distributions) ────────────────────────────────────────

def plot_pairplot(df: pd.DataFrame, sample_n: int = 600):
    """
    Plot pairwise joint distributions of N, P, K, pH.
    Sampling keeps rendering fast for large datasets.
    """
    features = ["n", "p", "k", "ph", "crop"]
    subset   = df[features].sample(n=min(sample_n, len(df)), random_state=42)

    # Limit to top-6 crops for readability
    top_crops = subset["crop"].value_counts().head(6).index
    subset    = subset[subset["crop"].isin(top_crops)]

    g = sns.pairplot(
        subset,
        hue="crop",
        vars=["n", "p", "k", "ph"],
        diag_kind="kde",
        plot_kws={"alpha": 0.5, "s": 20},
        palette="tab10",
    )
    g.figure.suptitle("Joint Distribution of Soil Features by Crop", y=1.02, fontsize=14)
    plt.tight_layout()
    plt.savefig("models/pairplot.png", dpi=120)
    plt.show()
    print("Pairplot saved to models/pairplot.png")


# ── 2. Correlation Heatmap ───────────────────────────────────────────────────

def plot_correlation(df: pd.DataFrame):
    features = ["n", "p", "k", "ph"]
    corr     = df[features].corr()

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=13)
    plt.tight_layout()
    plt.savefig("models/correlation_heatmap.png", dpi=150)
    plt.show()
    print("Correlation heatmap saved to models/correlation_heatmap.png")


# ── 3. Feature Importance ────────────────────────────────────────────────────

def plot_feature_importance(model, feature_names: list):
    # Works for both DecisionTree and RandomForest
    importances = model.feature_importances_
    indices     = np.argsort(importances)[::-1]
    sorted_feat = [feature_names[i] for i in indices]
    sorted_imp  = importances[indices]

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#4CAF50" if v == max(sorted_imp) else "#81C784" for v in sorted_imp]
    ax.barh(sorted_feat[::-1], sorted_imp[::-1], color=colors[::-1], edgecolor="white")
    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance for Crop Prediction")
    plt.tight_layout()
    plt.savefig("models/feature_importance.png", dpi=150)
    plt.show()
    print("Feature importance chart saved to models/feature_importance.png")


# ── 4. Decision Tree Structure ───────────────────────────────────────────────

def plot_decision_tree(le, feature_names: list):
    """
    Train a shallow Decision Tree purely for visualisation
    (depth=4 keeps the plot readable).
    """
    df_vis = load_data()
    df_vis, _ = encode_labels(df_vis)

    feature_cols = ["n", "p", "k", "ph"]
    X = df_vis[feature_cols]
    y = df_vis["crop_encoded"]

    dt_vis = DecisionTreeClassifier(max_depth=4, random_state=42)
    dt_vis.fit(X, y)

    fig, ax = plt.subplots(figsize=(22, 10))
    plot_tree(
        dt_vis,
        feature_names=feature_names,
        class_names=le.classes_,
        filled=True,
        rounded=True,
        fontsize=8,
        ax=ax,
        impurity=False,
        proportion=True,
    )
    ax.set_title("Decision Tree (depth = 4) — Crop Recommendation", fontsize=14)
    plt.tight_layout()
    plt.savefig("models/decision_tree.png", dpi=120)
    plt.show()
    print("Decision tree diagram saved to models/decision_tree.png")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = load_data()
    df, le = encode_labels(df)

    model, le_loaded = load_model()
    feature_names    = ["N", "P", "K", "pH"]

    print("\n[1/4] Generating pairplot ...")
    plot_pairplot(df)

    print("\n[2/4] Generating correlation heatmap ...")
    plot_correlation(df)

    print("\n[3/4] Generating feature importance chart ...")
    plot_feature_importance(model, feature_names)

    print("\n[4/4] Generating decision tree diagram ...")
    plot_decision_tree(le_loaded, feature_names)

    print("\nAll visualisations generated successfully.")
