import os
import joblib
from model.fallback import danger_score as fallback_score

# Construct path to the model file
model_path = os.path.join(os.path.dirname(__file__), '..', 'danger_score_model.pkl')

# Attempt to load the model and vectorizer
try:
    vectorizer, model = joblib.load(model_path)
    print("✅ ML danger scoring model loaded successfully.")
except Exception as e:
    print(f"⚠️ Failed to load danger_score_model.pkl: {e}")
    vectorizer, model = None, None

def score_transcript(transcript: str) -> float:
    """
    Computes danger score using trained ML model.
    Falls back to keyword scoring if model is unavailable or inference fails.
    """
    if model is None or vectorizer is None:
        print("⚠️ Using fallback (keyword-based) danger score.")
        return fallback_score(transcript)

    try:
        features = vectorizer.transform([transcript])
        proba = model.predict_proba(features)[0][1]  # Probability of class 1 (danger)
        print(f"✅ ML model predicted danger probability: {proba:.2f}")
        return round(proba, 2)
    except Exception as e:
        print(f"⚠️ Model inference failed: {e}")
        return fallback_score(transcript)
