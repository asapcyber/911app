# model/train_pipeline.py
from model.db import SessionLocal
from model.models import CallRecord
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def train_model_from_db():
    session = SessionLocal()
    calls = session.query(CallRecord).all()

    if not calls:
        print("No records found in DB.")
        return

    transcripts = [call.transcript for call in calls]
    labels = [call.danger_score for call in calls]

    # Use Dutch stopwords
    from nltk.corpus import stopwords
    dutch_stopwords = stopwords.words('dutch')

    vectorizer = TfidfVectorizer(stop_words=dutch_stopwords, max_features=500)
    X = vectorizer.fit_transform(transcripts)

    model = RandomForestRegressor()
    model.fit(X, labels)

    # Save both model and vectorizer
    joblib.dump((vectorizer, model), "danger_score_model.pkl")
    print("✅ Model and vectorizer saved to danger_score_model.pkl")

if __name__ == "__main__":
    train_model_from_db()
