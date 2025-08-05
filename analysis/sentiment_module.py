f# analysis/sentiment_module.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

# Basic Dutch emotion terms
DUTCH_EMOTIONS = {
    "angst": "Angst",
    "bang": "Angst",
    "boos": "Boosheid",
    "kwaad": "Boosheid",
    "verdriet": "Verdriet",
    "huilen": "Verdriet",
    "paniek": "Paniek",
    "stress": "Stress",
    "geschreeuw": "Stress",
    "rustig": "Kalmte",
    "blij": "Vreugde",
    "gelukkig": "Vreugde"
}

def detect_dutch_emotions(text):
    found = []
    lower_text = text.lower()
    for word, label in DUTCH_EMOTIONS.items():
        if word in lower_text:
            found.append(label)
    return list(set(found)) or ["Geen specifieke emotie herkend"]

def sentiment_analysis(transcript: str):
    sia = SentimentIntensityAnalyzer()
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    sentiments = []
    emotions = []

    for line in lines:
        blob = TextBlob(line)
        emotion = sia.polarity_scores(line)
        detected_emotions = detect_dutch_emotions(line)
        emotions.extend(detected_emotions)
        sentiments.append({
            'Lijn': line,
            'Polarity': blob.sentiment.polarity,
            'Subjectivity': blob.sentiment.subjectivity,
            'Negatief': emotion['neg'],
            'Neutraal': emotion['neu'],
            'Positief': emotion['pos'],
            'Totaal': emotion['compound']
        })

    df = pd.DataFrame(sentiments)
    unique_emotions = list(set(emotions))
    return df, unique_emotions

def plot_sentiment_chart(sentiment_df: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sentiment_df, x=sentiment_df.index, y='Polarity', label='Polarity', marker='o')
    sns.lineplot(data=sentiment_df, x=sentiment_df.index, y='Subjectivity', label='Subjectivity', marker='o')
    sns.lineplot(data=sentiment_df, x=sentiment_df.index, y='Totaal', label='Gevoelscore (compound)', marker='o')
    plt.title('Sentiment & Emotie Analyse van Transcript')
    plt.xlabel('Lijnnummer')
    plt.ylabel('Score')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    return plt
