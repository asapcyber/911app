import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from model.scoring import score_transcript
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NLTK resource handling (safe for Streamlit Cloud)
import os
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)

DUTCH_STOP_WORDS = stopwords.words('dutch')

# --- Extract Dutch keywords dynamically --- #
def extract_dutch_keywords(transcript, top_n=10):
    try:
        tokens = word_tokenize(transcript.lower())  # Avoid language='dutch'
        cleaned_text = " ".join([
            t for t in tokens if t.isalpha() and t not in DUTCH_STOP_WORDS
        ])
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([cleaned_text])
        scores = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
        sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)
        keywords = [kw for kw, _ in sorted_keywords[:top_n]]
        logger.info(f"Extracted Dutch keywords: {keywords}")
        return keywords
    except Exception as e:
        logger.error(f"Keyword extraction failed: {e}")
        return []

# --- Run sensitivity by perturbing key Dutch terms --- #
def run_sensitivity_analysis(transcript: str):
    base_score = score_transcript(transcript)
    keywords = extract_dutch_keywords(transcript)
    results = []

    for word in keywords:
        modified = transcript.replace(word, "")
        new_score = score_transcript(modified)
        delta = round(new_score - base_score, 2)
        results.append({
            "Scenario": f"Verwijder '{word}'",
            "Δ Change": delta,
            "Color": "red" if delta < 0 else "green"
        })

    logger.info(f"Sensitivity results: {results}")
    return results

# --- Plot the sensitivity chart --- #
def plot_sensitivity_chart(results):
    df = pd.DataFrame(results)
    if df.empty:
        return

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Δ Change', y='Scenario', hue='Color', dodge=False, palette={"red": "red", "green": "green"})
    plt.axvline(0, color='gray', linestyle='--')
    plt.title('Gevoeligheidsanalyse: Impact van Termen op Gevaarscore')
    plt.xlabel('Verandering in Score')
    plt.ylabel('Scenario')
    plt.legend(title='Impact')
    plt.tight_layout()
    return plt
