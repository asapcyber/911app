# model/train_pipeline.py
"""
Trainingspipeline voor 112-gevaarscore:
- Leest data uit DB (CallRecord)
- TF-IDF (nl stopwoorden, ngram_range=(1,2))
- Ridge-regressie voor score 0..1
- Slaat model op als model/danger_score_model.pkl

Run:
    python -m model.train_pipeline
of:
    python model/train_pipeline.py
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Project imports
from model.db import SessionLocal
from model.models import CallRecord

# NLTK stopwoorden NL
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)
DUTCH_STOP = set(stopwords.words('dutch'))

MODEL_PATH = os.path.join(os.path.dirname(__file__), "danger_score_model.pkl")


def _fetch_data_from_db() -> pd.DataFrame:
    """Haal alle transcripts + danger_score op uit de DB."""
    session = SessionLocal()
    try:
        rows = session.query(CallRecord).all()
        data = [{
            "transcript": r.transcript or "",
            "danger_score": float(r.danger_score) if r.danger_score is not None else np.nan
        } for r in rows]
    finally:
        session.close()
    df = pd.DataFrame(data)
    # Alleen rijen met geldige transcript + danger_score
    df = df.dropna(subset=["transcript", "danger_score"])
    df = df[df["transcript"].str.strip().astype(bool)]
    return df


def _build_pipeline() -> Pipeline:
    """Bouw de ML pipeline: TF-IDF (1,2-grams) + Ridge regression."""
    vectorizer = TfidfVectorizer(
        stop_words=list(DUTCH_STOP),
        ngram_range=(1, 2),
        max_features=5000,
        lowercase=True,
        strip_accents="unicode"
    )
    model = Ridge(alpha=1.0, random_state=42)
    pipe = Pipeline([
        ("tfidf", vectorizer),
        ("reg", model)
    ])
    return pipe


def _print_vocab_presence(pipe: Pipeline, terms: List[str]):
    """Check of bepaalde risicotermen in de vocab staan (voor debugging/kwaliteitscontrole)."""
    try:
        vect: TfidfVectorizer = pipe.named_steps["tfidf"]
        vocab = vect.vocabulary_ or {}
        found = [t for t in terms if t in vocab]
        missing = [t for t in terms if t not in vocab]
        print("🔎 Vocab check — Aanwezig:", found)
        print("🔎 Vocab check — Ontbrekend:", missing)
    except Exception as e:
        print(f"⚠️ Kon vocab niet controleren: {e}")


def train_model_from_db(save_path: str = MODEL_PATH) -> Tuple[Pipeline, dict]:
    """Train het model op DB-data en sla op."""
    df = _fetch_data_from_db()
    if df.empty:
        raise ValueError("Geen trainingsdata gevonden in de database.")

    X = df["transcript"].tolist()
    y = df["danger_score"].astype(float).clip(0, 1).values

    # Train/val-split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )

    pipe = _build_pipeline()
    pipe.fit(X_train, y_train)

    # Evaluatie
    y_pred = pipe.predict(X_val)
    metrics = {
        "r2": float(r2_score(y_val, y_pred)),
        "mae": float(mean_absolute_error(y_val, y_pred)),
        "n_train": int(len(X_train)),
        "n_val": int(len(X_val))
    }
    print(f"✅ Model getraind — R²: {metrics['r2']:.3f}, MAE: {metrics['mae']:.3f} "
          f"(train {metrics['n_train']}, val {metrics['n_val']})")

    # Controleer vocab op kerntermen (ook bigram)
    vocab_terms = ["mes", "bedreigt", "snijdt", "met een mes", "bedreigt iedereen"]
    _print_vocab_presence(pipe, vocab_terms)

    # Opslaan
    joblib.dump(pipe, save_path)
    print(f"💾 Opgeslagen naar: {save_path}")

    return pipe, metrics


# Backwards-compat alias, indien de app dit aanroept:
def retrain_model_from_db():
    return train_model_from_db(MODEL_PATH)


if __name__ == "__main__":
    train_model_from_db(MODEL_PATH)
