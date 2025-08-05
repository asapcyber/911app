# train_pipeline.py

from model.db import SessionLocal
from model.models import CallRecord
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd

# Step 1: Load from DB
db = SessionLocal()
records = db.query(CallRecord).all()
db.close()

# Step 2: Convert ORM objects to usable dict format
call_data = [{
    'transcript': r.transcript,
    'danger_score': r.danger_score
} for r in records]

df = pd.DataFrame(call_data)

# Step 3: Train pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=500)),
    ('model', DecisionTreeRegressor())
])

pipeline.fit(df['transcript'], df['danger_score'])

# Step 4: Save model
joblib.dump(pipeline, 'danger_score_model.pkl')
print("✅ New danger_score_model.pkl created.")
