import pandas as pd
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error
import joblib

# Simulate 911 dataset
def simulate_911_data_with_threat(num_samples=500):
    weapons = ['knife', 'gun', 'none']
    actions = ['cutting', 'yelling', 'fleeing', 'calm']
    mental_state = ['agitated', 'crying', 'calm', 'panicked']
    past_violence = ['yes', 'no']
    police_history = ['frequent', 'none', 'occasional']
    threat_type = ['verbal', 'physical', 'online', 'none']

    data = []
    for _ in range(num_samples):
        weapon = random.choice(weapons)
        action = random.choice(actions)
        mental = random.choice(mental_state)
        violence = random.choice(past_violence)
        police = random.choice(police_history)
        threat = random.choice(threat_type)

        score = 0
        if weapon == 'gun':
            score += 0.4
        elif weapon == 'knife':
            score += 0.3
        if action in ['cutting', 'fleeing']:
            score += 0.2
        if mental in ['agitated', 'panicked']:
            score += 0.2
        if violence == 'yes':
            score += 0.1
        if police == 'frequent':
            score += 0.1
        if threat == 'physical':
            score += 0.2
        elif threat == 'verbal':
            score += 0.1
        elif threat == 'online':
            score += 0.05

        data.append({
            'weapon': weapon,
            'action': action,
            'mental_state': mental,
            'past_violence': violence,
            'police_history': police,
            'threat': threat,
            'danger_score': round(min(score, 1.0), 2)
        })
    return pd.DataFrame(data)

# Create and split data
df = simulate_911_data_with_threat()
X = df.drop(columns=['danger_score'])
y = df['danger_score']

# Categorical features
categorical_features = X.columns.tolist()
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)]
)

# Build pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
mse = mean_squared_error(y_test, preds)
print(f"Model trained. MSE: {mse:.4f}")

# Save model
joblib.dump(pipeline, "danger_score_model.pkl")
print("Model saved as danger_score_model.pkl")
