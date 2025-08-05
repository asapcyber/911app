from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model.models import Call
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

# Connect to the DB
engine = create_engine('sqlite:///112_calls.db')
Session = sessionmaker(bind=engine)
session = Session()

# Fetch training data
def fetch_training_data():
    calls = session.query(Call).all()
    data = []
    for call in calls:
        data.append({
            "transcript": call.transcript,
            "danger_score": call.danger_score
        })
    return pd.DataFrame(data)

df = fetch_training_data()

# Train model
X = df['transcript']
y = df['danger_score']

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("model", RandomForestRegressor(n_estimators=100, random_state=42))
])

pipeline.fit(X, y)

# Save to file
joblib.dump(pipeline, "danger_score_model.pkl")
print("✅ danger_score_model.pkl updated successfully!")
