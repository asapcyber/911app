import re
from typing import List, Dict
from model.scoring import score_transcript
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def run_sensitivity_analysis(transcript: str) -> List[Dict[str, str]]:
    """
    Generates variations of the transcript and evaluates danger score changes using the ML model.
    """
    base_score = score_transcript(transcript)

    variants = [
        ("Remove 'knife'", re.sub(r'\bknife\b', '', transcript, flags=re.I)),
        ("Remove 'cutting herself'", re.sub(r'cutting herself', '', transcript, flags=re.I)),
        ("Remove 'stab me'", re.sub(r'stab.*', '', transcript, flags=re.I)),
        ("Remove fleeing language", re.sub(r'\bflee\b|\brun\b|\bdrove away\b', '', transcript, flags=re.I)),
        ("Remove reference to police", re.sub(r'police.*?times', '', transcript, flags=re.I)),
        ("Replace 'crazy' with 'confused'", re.sub(r'crazy', 'confused', transcript, flags=re.I)),
        ("Tone made calmer", re.sub(r'i have to run.*', 'She may be unstable, but I’m okay.', transcript, flags=re.I))
    ]

    results = []
    for label, modified in variants:
        new_score = score_transcript(modified)
        delta = round(new_score - base_score, 2)
        results.append({
            "Scenario": label,
            "Danger Score": round(new_score, 2),
            "Δ Change": delta
        })

    return results

def plot_sensitivity_chart(results: List[Dict[str, str]]):
    df = pd.DataFrame(results)
    df['Color'] = df['Δ Change'].apply(lambda x: 'green' if x < 0 else 'red')

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Δ Change', y='Scenario', palette=df['Color'])
    plt.axvline(0, color='gray', linestyle='--')
    plt.title("🔍 Sensitivity Analysis Impact on Danger Score")
    plt.xlabel("Change in Score")
    plt.ylabel("Scenario")
    st.pyplot(plt)


