import pandas as pd
import random
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Train model inline at load time
def train_model():
    def simulate_data(n=200):
        weapons = ['knife', 'gun', 'none']
        actions = ['cutting', 'yelling', 'fleeing', 'calm']
        mental_state = ['agitated', 'crying', 'calm', 'panicked']
        past_violence = ['yes', 'no']
        police_history = ['frequent', 'none', 'occasional']
        threat = ['verbal', 'physical', 'online', 'none']
        data = []
        for _ in range(n):
            w, a, m, v, p, t = random.choice(weapons), random.choice(actions), random.choice(mental_state), \
                               random.choice(past_violence), random.choice(police_history), random.choice(threat)
            score = 0
            score += {'gun': 0.4, 'knife': 0.3, 'none': 0}[w]
            score += {'cutting': 0.2, 'fleeing': 0.2, 'yelling': 0.1, 'calm': 0}[a]
            score += {'agitated': 0.2, 'panicked': 0.2, 'crying': 0.1, 'calm': 0}[m]
            score += {'yes': 0.1, 'no': 0}[v]
            score += {'frequent': 0.1, 'occasional': 0.05, 'none': 0}[p]
            score += {'physical': 0.2, 'verbal': 0.1, 'online': 0.05, 'none': 0}[t]
            data.append({
                'weapon': w, 'action': a, 'mental_state': m,
                'past_violence': v, 'police_history': p, 'threat': t,
                'danger_score': round(min(score, 1.0), 2)
            })
        return pd.DataFrame(data)

    df = simulate_data()
    X = df.drop(columns='danger_score')
    y = df['danger_score']
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(), X.columns.tolist())
    ])
    model = Pipeline([
        ("pre", preprocessor),
        ("gb", GradientBoostingRegressor(n_estimators=100, random_state=42))
    ])
    model.fit(X, y)
    return model

# Global model loaded at runtime
model = train_model()

def score_transcript(features: dict) -> float:
    """Takes a dict of features and returns a danger score (0–1)."""
    X_input = pd.DataFrame([features])
    return float(model.predict(X_input)[0])
