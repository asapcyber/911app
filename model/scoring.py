# model/scoring.py

import joblib
import os
from sklearn.base import BaseEstimator
from typing import Optional

# Load danger scoring model
model_path = os.path.join(os.path.dirname(__file__), "..", "danger_score_model.pkl")

try:
    model: Optional[BaseEstimator] = joblib.load(model_path)
except Exception as e:
    print(f"[!] Failed to load ML model: {e}")
    model = None

def score_transcript(transcript: str) -> float:
    """
    Predicts the danger score (between 0.0 and 1.0) based on the transcript using trained ML model.
    Falls back to keyword-based scoring if model isn't available.
    """
    if model:
        try:
            score = float(model.predict([transcript])[0])
            return round(score, 2)
        except Exception as e:
            print(f"[!] ML prediction failed: {e}")

    # Fallback: Keyword-based heuristic
    fallback_keywords = ["knife", "threat", "gun", "stab", "kill", "blood", "flee", "abuse"]
    danger_score = sum(1 for kw in fallback_keywords if kw in transcript.lower()) / len(fallback_keywords)
    return round(danger_score, 2)

