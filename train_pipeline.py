# train_pipeline.py

from model.db import SessionLocal
from model.models import CallRecord
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import pandas as pd

# Custom transformer to extract 'transcript' column
class TextSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.key]

# Step 1: Load records from DB
db = SessionLocal()
records = db.query(CallRecord).all()
db.close()

# Step 2: Convert to DataFrame
call_data = [{
    'transcript': r.transcript,
    'threat_type': r.threat_type,
    'danger_score': r.danger_score
} for r in records]

df = pd.DataFrame(call_data)

# Step 3: Define pipeline
preprocessor = ColumnTransformer(transformers=[
    ('text', TfidfVectorizer(max_features=500), 'transcript'),
    ('threat', OneHotEncoder(handle_unknown='ignore'), ['threat_type'])
])

pipeline = Pipeline([
    ('features', preprocessor),
    ('model', DecisionTreeRegressor())
])

# Step 4: Train model
pipeline.fit(df[['transcript', 'threat_type']], df['danger_score'])

# Step 5: Save model
joblib.dump(pipeline, 'danger_score_model.pkl')
print("✅ Model with 'threat_type' saved to danger_score_model.pkl")
