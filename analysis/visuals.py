# analysis/visuals.py

import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.data import find

def plot_risk_factors(transcript: str):
    try:
        find('tokenizers/punkt')
    except LookupError:
        print("❌ NLTK 'punkt' tokenizer not found. Risk factor chart will be skipped.")
        return None

    if not isinstance(transcript, str):
        return None

    try:
        tokens = [word for word in word_tokenize(transcript.lower()) if word.isalpha()]
        word_freq = nltk.FreqDist(tokens)
        common_words = word_freq.most_common(10)

        if not common_words:
            return None

        words, freqs = zip(*common_words)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(words[::-1], freqs[::-1])
        ax.set_title("🔍 Meest Voorkomende Woorden in Transcript")
        ax.set_xlabel("Frequentie")
        plt.tight_layout()
        return fig

    except Exception as e:
        print(f"⚠️ Fout bij het plotten van risicofactoren: {e}")
        return None
