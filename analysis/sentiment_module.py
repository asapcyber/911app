import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import streamlit as st

nltk.download('vader_lexicon', quiet=True)

def sentiment_analysis(transcript: str) -> pd.DataFrame:
    sia = SentimentIntensityAnalyzer()
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    sentiments = []
    for line in lines:
        blob = TextBlob(line)
        emotion = sia.polarity_scores(line)
        sentiments.append({
            'Line': line,
            'Polarity': blob.sentiment.polarity,
            'Subjectivity': blob.sentiment.subjectivity,
            'Neg': emotion['neg'],
            'Neu': emotion['neu'],
            'Pos': emotion['pos'],
            'Compound': emotion['compound']
        })
    return pd.DataFrame(sentiments)

def plot_sentiment_chart(sentiment_df: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sentiment_df, x=sentiment_df.index, y='Polarity', label='Polarity', marker='o')
    sns.lineplot(data=sentiment_df, x=sentiment_df.index, y='Subjectivity', label='Subjectivity', marker='o')
    sns.lineplot(data=sentiment_df, x=sentiment_df.index, y='Compound', label='Emotion (Compound)', marker='o')
    plt.title('Sentiment & Emotion Analysis of 911 Transcript')
    plt.xlabel('Line #')
    plt.ylabel('Score')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    st.pyplot(plt)

