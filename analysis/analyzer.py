# analysis/analyzer.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from model.scoring import score_transcript
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import logging


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK resources if not already
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

DUTCH_STOP_WORDS = set(stopwords.words('dutch'))

# --- Extract Dutch keywords dynamically with filtering --- #
def extract_dutch_keywords(transcript: str, top_n=10):
    logger.info("Extracting keywords from transcript...")

    tokens = word_tokenize(transcript.lower())
    filtered_tokens = [t for t in tokens if t.isalpha() and t not in DUTCH_STOP_WORDS]

    # Use POS tag filtering: keep nouns, verbs, adjectives (manually mapped, since NLTK POS tagging is English-based)
    tagged = pos_tag(filtered_tokens, lang='eng')  # Approximate tagging
    logger.info(f"POS Tagged tokens: {tagged}")

    keywords = [word for word, tag in tagged if tag.startswith('N') or tag.startswith('V') or tag.startswith('J')]
    keywords = list(set(keywords))  # Deduplicate

    if not keywords:
        # Fallback to TF-IDF if POS fails
        logger.warning("No relevant POS keywords found, falling back to TF-IDF.")
        vectorizer = TfidfVectorizer(stop_words=list(DUTCH_STOP_WORDS))
        X = vectorizer.fit_transform([transcript])
        scores = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
        sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)
        keywords = [kw for kw, _ in sorted_keywords[:top_n]]

    logger.info(f"Selected keywords for sensitivity: {keywords}")
    return keywords[:top_n]

# --- Run sensitivity by removing key Dutch terms --- #
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
