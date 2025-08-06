# app.py

import streamlit as st
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
from model.scoring import score_transcript
import matplotlib.pyplot as plt

st.set_page_config(page_title="112 Gevaarscore Analyzer", layout="wide")
st.title("🚨 112 Gevaarscore Analyzer")

user_input = st.text_area("Voer een 112-transcript in", height=200, placeholder="Bijv: Mijn vriend schreeuwt en bedreigt mij met een mes...")

tabs = st.tabs(["Incidentkaart", "Emotie & Risicoanalyse", "AI MCP Agent", "Admin (Model)"])

# --- Tab 1: Incident Card (Dutch) ---
with tabs[0]:
    if user_input:
        html_card = generate_incident_card(user_input)
        st.components.v1.html(html_card, height=400, scrolling=True)

# --- Tab 2: Sentiment & Risk (Dutch) ---
with tabs[1]:
    if user_input:
        st.subheader("📈 Emotionele Analyse en Risicofactoren")

        sentiment_df, emotions = sentiment_analysis(user_input)
        fig1 = plot_sentiment_chart(sentiment_df)
        if fig1:
            st.pyplot(fig1)

        fig2 = plot_risk_factors(user_input)
        if fig2:
            st.pyplot(fig2)

        st.write("**Gedetecteerde emoties en sentimenten:**")
        st.dataframe(sentiment_df)

# --- Tab 3: AI MCP Agent (Optional Placeholder) ---
with tabs[2]:
    st.info("🧠 MCP Agent niet geconfigureerd. Integratie volgt later.")

# --- Tab 4: Admin for Retraining ---
with tabs[3]:
    st.subheader("🔧 Adminpaneel voor ML Model")
    if st.button("Hertrain Model"):
        from model.training import retrain_model_from_db
        try:
            retrain_model_from_db()
            st.success("Model succesvol hertraind en opgeslagen als danger_score_model.pkl")
        except Exception as e:
            st.error(f"Fout bij hertrainen van model: {e}")
