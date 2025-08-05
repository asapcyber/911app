import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from model.scoring import score_transcript
import nltk
from nltk.corpus import stopwords

# Download stopwords once (NLTK will cache them)
nltk.download('stopwords')
DUTCH_STOP_WORDS = stopwords.words('dutch')

# --- Extract Dutch keywords dynamically --- #
def extract_dutch_keywords(transcript, top_n=10):
    vectorizer = TfidfVectorizer(stop_words=DUTCH_STOP_WORDS)
    X = vectorizer.fit_transform([transcript])
    scores = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
    sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_keywords[:top_n]]

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
