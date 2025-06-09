import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_risk_factors(transcript: str):
    features = {
        'knife': 0.2,
        'cutting herself': 0.2,
        'stab': 0.2,
        'flee': 0.15,
        'run': 0.1,
        'police': 0.05,
        'abused': 0.05,
        'crazy': 0.05,
        'dangerous': 0.05
    }

    transcript_lower = transcript.lower()
    presence = {k: (1 if k in transcript_lower else 0) for k in features}
    weighted_presence = {k: features[k] * presence[k] for k in features}

    df = pd.DataFrame(list(weighted_presence.items()), columns=['Risk Factor', 'Score'])
    df = df[df['Score'] > 0].sort_values(by='Score', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Score', y='Risk Factor', palette='Reds_r')
    plt.title('Risk Factor Contribution to Danger Score')
    st.pyplot(plt)

