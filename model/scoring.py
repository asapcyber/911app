import joblib
import pandas as pd
import os

# Load model once
model_path = "danger_score_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError("ML model not found. Please ensure danger_score_model.pkl exists.")
model = joblib.load(model_path)

# Extract structured features from transcript
def extract_features(transcript: str) -> pd.DataFrame:
    transcript = transcript.lower()
    features = {
        'weapon': 'none',
        'action': 'calm',
        'mental_state': 'calm',
        'past_violence': 'no',
        'police_history': 'none',
        'threat': 'none'
    }

    if 'gun' in transcript:
        features['weapon'] = 'gun'
    elif 'knife' in transcript:
        features['weapon'] = 'knife'

    if 'cutting' in transcript:
        features['action'] = 'cutting'
    elif 'yelling' in transcript:
        features['action'] = 'yelling'
    elif 'run' in transcript or 'flee' in transcript:
        features['action'] = 'fleeing'

    if 'panicked' in transcript or 'agitated' in transcript:
        features['mental_state'] = 'agitated'
    elif 'crying' in transcript:
        features['mental_state'] = 'crying'

    if 'abuse' in transcript or 'threatens me every day' in transcript or 'violent' in transcript:
        features['past_violence'] = 'yes'

    if 'police have been there many times' in transcript:
        features['police_history'] = 'frequent'
    elif 'police' in transcript:
        features['police_history'] = 'occasional'

    if 'stab' in transcript or 'threat' in transcript or 'danger' in transcript:
        features['threat'] = 'physical'
    elif 'scream' in transcript or 'yelling' in transcript:
        features['threat'] = 'verbal'
    elif 'online' in transcript:
        features['threat'] = 'online'

    return pd.DataFrame([features])

# Predict danger score from transcript
def score_transcript(transcript: str) -> float:
    features = extract_features(transcript)
    score = model.predict(features)[0]
    return round(float(score), 2)
