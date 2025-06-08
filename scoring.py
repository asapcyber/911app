import joblib
import pandas as pd

# Load the trained model
model = joblib.load("danger_score_model.pkl")

# Extract basic features from a 911 transcript
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

    if 'panicked' in transcript or 'panic' in transcript or 'agitated' in transcript:
        features['mental_state'] = 'agitated'
    elif 'crying' in transcript:
        features['mental_state'] = 'crying'

    if 'abuse' in transcript or 'violence' in transcript or 'threatens me every day' in transcript:
        features['past_violence'] = 'yes'

    if 'police have been there many times' in transcript:
        features['police_history'] = 'frequent'
    elif 'police' in transcript:
        features['police_history'] = 'occasional'

    if 'stab' in transcript or 'threatening' in transcript:
        features['threat'] = 'physical'
    elif 'scream' in transcript or 'yelling' in transcript:
        features['threat'] = 'verbal'
    elif 'online' in transcript:
        features['threat'] = 'online'

    return pd.DataFrame([features])

# Score the danger level using the trained model
def score_transcript(transcript: str) -> float:
    features_df = extract_features(transcript)
    score = model.predict(features_df)[0]
    return round(float(score), 2)
