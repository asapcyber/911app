# analysis/analyzer.py
import re
from typing import List, Dict
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model.scoring import model

def run_sensitivity_analysis(transcript: str) -> pd.DataFrame:
    """Returns dynamic top N contributing terms based on TF-IDF and model importance."""

    if not model or not hasattr(model.named_steps["model"], "feature_importances_"):
        return pd.DataFrame({
            "Scenario": ["ML model not available or does not support feature importance."],
            "Δ Change": [0.0],
            "Color": ["gray"]
        })

    tfidf = model.named_steps["tfidf"]
    regressor = model.named_steps["model"]

    # Transform transcript to get tf-idf vector
    tfidf_vector = tfidf.transform([transcript])
    feature_array = tfidf.get_feature_names_out()
    tfidf_values = tfidf_vector.toarray()[0]

    # Match TF-IDF score × feature importance
    importance_scores = []
    for i, score in enumerate(tfidf_values):
        if score > 0:
            term = feature_array[i]
            importance = regressor.feature_importances_[i] if i < len(regressor.feature_importances_) else 0
            impact = score * importance
            importance_scores.append((term, impact))

    top_features = sorted(importance_scores, key=lambda x: x[1], reverse=True)[:5]

    df = pd.DataFrame(top_features, columns=["Scenario", "Δ Change"])
    df["Color"] = ["red", "orange", "gold", "green", "blue"][:len(df)]

    return df

def plot_sensitivity_chart(df: pd.DataFrame):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4))

    # Plot bars manually to assign individual colors
    for i, row in df.iterrows():
        plt.barh(
            y=row["Scenario"],
            width=row["Δ Change"],
            color=row["Color"]
        )

    plt.xlabel("Δ Change")
    plt.title("Sensitivity Analysis – Top Risk Contributors")
    plt.tight_layout()
    st.pyplot(plt)
