import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy.orm import Session
from model.models import CallRecord
from model.db import SessionLocal

def retrain_model_from_db():
    session: Session = SessionLocal()
    records = session.query(CallRecord).all()

    if not records:
        raise ValueError("No call records found in database.")

    texts = [record.transcript for record in records]
    labels = [record.danger_score for record in records]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    y = labels

    model = RandomForestRegressor()
    model.fit(X, y)

    # Save model and vectorizer
    joblib.dump((vectorizer, model), "danger_score_model.pkl")

    return len(records)

