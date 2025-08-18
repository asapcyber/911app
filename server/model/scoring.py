# model/scoring.py
import joblib
import os

model_path = "danger_score_model.pkl"
vectorizer = None
model = None

# Load model and vectorizer at module load
if os.path.exists(model_path):
    vectorizer, model = joblib.load(model_path)
else:
    print("⚠️ danger_score_model.pkl not found. Please train the model first.")

def score_transcript(transcript: str) -> float:
    global vectorizer, model
    if not model or not vectorizer:
        raise RuntimeError("Model not loaded. Retrain using train_pipeline.py first.")
    
    X = vectorizer.transform([transcript])
    prediction = model.predict(X)[0]
    return round(float(prediction), 2)
