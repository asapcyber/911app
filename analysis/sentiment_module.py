# analysis/sentiment_module.py
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd

nltk.download('punkt')

def safe_sent_tokenize(text: str, lang='dutch'):
    try:
        return sent_tokenize(text, language=lang)
    except LookupError:
        # Fallback: split by period
        return text.split('.')

def sentiment_analysis(transcript: str):
    sentences = safe_sent_tokenize(transcript)
    emotions = []
    for sentence in sentences:
        blob = TextBlob(sentence)
        polarity = blob.sentiment.polarity
        emotions.append({
            "Sentence": sentence.strip(),
            "Polarity": round(polarity, 2)
        })
    df = pd.DataFrame(emotions)
    return df, None

def plot_sentiment_chart(sentiment_df: pd.DataFrame):
    if sentiment_df is None or sentiment_df.empty:
        return

    plt.figure(figsize=(10, 4))
    plt.plot(sentiment_df.index, sentiment_df["Polarity"], marker="o")
    plt.title("📈 Emotionele Polariteit per Zin")
    plt.xlabel("Zin Index")
    plt.ylabel("Polariteit (-1 tot 1)")
    plt.grid(True)
    plt.tight_layout()
