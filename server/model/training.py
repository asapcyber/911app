import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from model.db import SessionLocal
from model.models import CallRecord

def retrain_model_from_db():
    # Step 1: Pull all call records from DB
    db = SessionLocal()
    records = db.query(CallRecord).all()
    db.close()

    if not records:
        print("❌ No call records found in DB.")
        return

    # Step 2: Convert records to DataFrame
    data = [{
        "text": record.transcript,
        "danger_score": record.danger_score,
        "threat_type": record.threat_type or ""
    } for record in records]

    df = pd.DataFrame(data)

    # Step 3: Combine threat_type with transcript text for better feature representation
    df["combined_text"] = df["threat_type"] + " " + df["text"]

    # Step 4: Vectorize using TF-IDF on combined text
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["combined_text"])
    y = df["danger_score"]

    # Step 5: Train model
    model = RandomForestRegressor()
    model.fit(X, y)

    # Step 6: Save model and vectorizer
    joblib.dump((vectorizer, model), "danger_score_model.pkl")
    print("✅ New danger scoring model saved to danger_score_model.pkl")
