# analysis/sentiment_module.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

# --- Dutch emotion keywords --- #
DUTCH_EMOTION_KEYWORDS = {
    'angst': ['bang', 'angstig', 'vrezen', 'paniek', 'beven'],
    'woede': ['boos', 'woedend', 'kwaad', 'razend', 'schreeuwen'],
    'verdriet': ['verdrietig', 'huilen', 'bedroefd', 'depressief'],
    'blijheid': ['blij', 'gelukkig', 'lachen', 'opgelucht'],
    'verrassing': ['verrast', 'verbazing', 'oh', 'wauw'],
    'walging': ['walgelijk', 'vies', 'afschuw', 'afkeer']
}

def sentiment_analysis(transcript: str):
    sentences = sent_tokenize(transcript, language='dutch')
    polarity_scores = []
    emotion_counts = {k: 0 for k in DUTCH_EMOTION_KEYWORDS.keys()}

    for idx, sentence in enumerate(sentences):
        blob = TextBlob(sentence)
        polarity = blob.sentiment.polarity
        polarity_scores.append({'Zin': idx + 1, 'Polarity': polarity})

        sentence_lower = sentence.lower()
        for emotion, keywords in DUTCH_EMOTION_KEYWORDS.items():
            if any(kw in sentence_lower for kw in keywords):
                emotion_counts[emotion] += 1

    sentiment_df = pd.DataFrame(polarity_scores)
    emotion_df = pd.DataFrame(list(emotion_counts.items()), columns=['Emotie', 'Aantal'])

    return sentiment_df, emotion_df

def plot_sentiment_chart(sentiment_df):
    if not isinstance(sentiment_df, pd.DataFrame) or sentiment_df.empty:
        print("❌ Geen geldige sentimentgegevens om te plotten.")
        return

    try:
        plt.figure(figsize=(10, 5))
        sns.lineplot(
            data=sentiment_df,
            x='Zin',
            y='Polarity',
            label='Polarity',
            marker='o'
        )
        plt.axhline(0, color='gray', linestyle='--')
        plt.title("Emotionele Polariteit van de Oproep")
        plt.xlabel("Zin Nummer")
        plt.ylabel("Polariteit")
        plt.legend()
        plt.tight_layout()
        st.pyplot(plt)
    except Exception as e:
        print(f"📉 Fout bij het plotten van sentiment: {e}")

def plot_emotion_chart(emotion_df):
    if not isinstance(emotion_df, pd.DataFrame) or emotion_df.empty:
        return

    try:
        plt.figure(figsize=(8, 5))
        sns.barplot(data=emotion_df, x='Emotie', y='Aantal', palette='pastel')
        plt.title("Gedetecteerde Emoties in de Transcriptie")
        plt.xlabel("Emotie")
        plt.ylabel("Aantal")
        plt.tight_layout()
        st.pyplot(plt)
    except Exception as e:
        print(f"📊 Fout bij het plotten van emoties: {e}")
