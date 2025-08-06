# app.py

import os
import streamlit as st
import requests
from model.scoring import score_transcript
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
from model.training import retrain_model_from_db

st.set_page_config(page_title="112 Gevaarscore Analyser", layout="wide")

st.title("🚨 112 Gevaarscore Analyser (NL)")
st.markdown("""
Deze applicatie analyseert meldingen bij de hulpdiensten (zoals 112) om het risico in te schatten,
gevoeligheden te evalueren, en hulpdiensten te ondersteunen met inzichten en aanbevelingen.
""")

# --- Input
user_input = st.text_area("📞 Voer hier de 112 transcriptie in:", height=250)

# --- Tabs
tab_labels = [
    "📋 Incidentkaart",
    "📊 Sentiment & Risico",
    "🛠️ Admin Paneel",
    "🧠 MCP Agent"
]
tabs = st.tabs(tab_labels)

# --- TAB 1: Incidentkaart --- #
with tabs[0]:
    if user_input:
        score = score_transcript(user_input)
        st.markdown(f"### 🔥 Gevaarscore: `{score:.2f}` (0 = Laag risico, 1 = Hoog risico)`")

        st.markdown("### 🧾 Incidentkaart")
        html_card = generate_incident_card(user_input)
        st.components.v1.html(html_card, height=800, scrolling=True)

        st.markdown("### 📉 Gevoeligheidsanalyse")
        results = run_sensitivity_analysis(user_input)
        if results:
            plot_sensitivity_chart(results)
        else:
            st.info("Geen belangrijke termen gevonden voor gevoeligheidsanalyse.")

# --- TAB 2: Sentiment & Risico Analyse --- #
with tabs[1]:
    if user_input:
        sentiment_df, emotion_df = sentiment_analysis(user_input)

        st.markdown("### 😐 Sentimentanalyse per regel")
        st.dataframe(sentiment_df)
        plot_sentiment_chart(emotion_df)

        st.markdown("### ⚠️ Risicofactoren (model-gedreven)")
        plot_risk_factors(user_input)

# --- TAB 3: Admin Panel (Model Retraining) --- #
with tabs[2]:
    st.markdown("### 🔄 Model Hertrainen met nieuwe database")
    st.info("Gebruik deze knop om het gevaarscore-model opnieuw te trainen op basis van alle gegevens in de database.")

    if st.button("Hertrain model"):
        retrain_model_from_db()
        st.success("Model is succesvol hertraind en opgeslagen als danger_score_model.pkl.")

# --- TAB 4: MCP Agent (OpenAI Assistant) --- #
with tabs[3]:
    st.markdown("### 🧠 MCP Agent – Vraag advies over het incident")
    mcp_query = st.text_input("Vraag van dispatcher of hulpverlener", placeholder="Bijv. De melder is gevlucht – wat nu?")
    if mcp_query and user_input:
        try:
            response = requests.post("http://localhost:8000/query", json={
                "query": mcp_query,
                "context": user_input
            })
            if response.status_code == 200:
                st.markdown(f"**🧠 Antwoord van de AI Agent:** {response.json()['response']}")
            else:
                st.error(f"Fout bij ophalen van AI antwoord: {response.text}")
        except Exception as e:
            st.error(f"Kon geen verbinding maken met MCP Agent. Draait deze lokaal? Foutmelding: {e}")
