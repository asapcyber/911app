# analysis/analyzer.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from model.scoring import score_transcript
from model.db import SessionLocal
from model.models import CallRecord

# Ensure NLTK components are downloaded
nltk.download('stopwords')
nltk.download('punkt')

DUTCH_STOP_WORDS = stopwords.words('dutch')

# --- Extract Dutch keywords dynamically using TF-IDF trained on DB corpus --- #
def extract_dutch_keywords(transcript: str, top_n: int = 10):
    print("[TF-IDF] Extracting Dutch keywords based on full corpus...")
    db = SessionLocal()
    records = db.query(CallRecord).all()
    db.close()

    corpus = [r.transcript for r in records if r.transcript and isinstance(r.transcript, str)]
    corpus.append(transcript)

    vectorizer = TfidfVectorizer(stop_words=DUTCH_STOP_WORDS)
    X = vectorizer.fit_transform(corpus)

    # Use the last (current) document
    current_vector = X[-1].toarray()[0]
    feature_names = vectorizer.get_feature_names_out()
    scores = zip(feature_names, current_vector)

    sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, score in sorted_keywords[:top_n] if kw.strip()]
    
    print(f"[TF-IDF] Top {top_n} keywords: {top_keywords}")
    return top_keywords

# --- Sensitivity Analysis by perturbing high-weight keywords --- #
def run_sensitivity_analysis(transcript: str):
    base_score = score_transcript(transcript)
    print(f"[Sensitiviteit] Basis score: {base_score}")

    keywords = extract_dutch_keywords(transcript)
    if not keywords:
        print("[Sensitiviteit] Geen gevoelige termen gevonden.")
        return []

    results = []
    for word in keywords:
        modified_transcript = transcript.replace(word, "")
        new_score = score_transcript(modified_transcript)
        delta = round(new_score - base_score, 2)

        results.append({
            "Scenario": f"Verwijder '{word}'",
            "Δ Change": delta,
            "Color": "red" if delta < 0 else "green"
        })

        print(f"[Sensitiviteit] '{word}' verwijderd → Δ {delta}")

    return results

# --- Plot the sensitivity chart --- #
def plot_sensitivity_chart(results):
    if not results:
        print("[Visualisatie] Geen resultaten voor gevoeligheidsanalyse.")
        return None

    df = pd.DataFrame(results)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Δ Change', y='Scenario', hue='Color', dodge=False,
                palette={"red": "red", "green": "green"})
    plt.axvline(0, color='gray', linestyle='--')
    plt.title('Gevoeligheidsanalyse: Impact van Termen op Gevaarscore')
    plt.xlabel('Verandering in Score')
    plt.ylabel('Scenario')
    plt.legend(title='Impact')
    plt.tight_layout()
    print("[Visualisatie] Gevoeligheidsgrafiek gegenereerd.")
    return plt.gcf()
