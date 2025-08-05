import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from model.scoring import danger_score
from sklearn.feature_extraction.text import TfidfVectorizer

# Dynamically extract Dutch keywords
def extract_dutch_keywords(transcript, top_n=5):
    vectorizer = TfidfVectorizer(stop_words="dutch", max_features=50)
    X = vectorizer.fit_transform([transcript])
    tfidf_scores = dict(zip(vectorizer.get_feature_names_out(), X.toarray()[0]))
    sorted_keywords = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, score in sorted_keywords[:top_n]]

# Run dynamic sensitivity analysis using Dutch keywords
def run_sensitivity_analysis(transcript):
    base_score = danger_score(transcript)
    keywords = extract_dutch_keywords(transcript)
    results = []

    for word in keywords:
        modified = transcript.replace(word, "")
        new_score = danger_score(modified)
        delta = round(base_score - new_score, 2)
        color = "red" if delta > 0.1 else "orange" if delta > 0.05 else "green"
        results.append({
            "Scenario": f"Zonder '{word}'",
            "Danger Score": round(new_score, 2),
            "Δ Change": delta,
            "Color": color
        })

    return results

# Sensitivity chart
def plot_sensitivity_chart(results):
    df = pd.DataFrame(results)
    plt.figure(figsize=(8, 4))
    sns.barplot(data=df, x="Δ Change", y="Scenario", palette=df["Color"].tolist())
    plt.title("Gevoeligheidsanalyse van het Gevaar Score")
    st.pyplot(plt)
