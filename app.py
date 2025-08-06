import streamlit as st
import requests
from model.scoring import score_transcript
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
from model.training import retrain_model_from_db

st.set_page_config(page_title="112 Analyse App", layout="wide")

st.title("🚨 112 Analyse Applicatie")
st.markdown("Beoordeel inkomende 112-oproepen op risico, sentiment en volgende acties.")

# Tabs
tabs = st.tabs([
    "📞 Analyseer 112 Oproep",
    "🧠 MCP Agent",
    "📋 Incidentkaart",
    "💬 Sentiment & Risico",
    "🛠️ Admin - Hertrain Model"
])

# --- TAB 1: Analyseer 112 Oproep ---
with tabs[0]:
    st.subheader("Transcript invoeren")
    user_input = st.text_area("Plak hier de transcriptie van de 112-oproep", height=300)

    if user_input:
        # 1. Score
        score = score_transcript(user_input)
        st.success(f"Gevaar Score: **{score:.2f}** (0 = Laag risico, 1 = Hoog risico)")

        # 2. Sensitivity
        st.subheader("🔍 Gevoeligheidsanalyse")
        results = run_sensitivity_analysis(user_input)
        st.write("DEBUG: Sensitivity Results", results)
        plot_sensitivity_chart(results)

# --- TAB 2: MCP Agent Interface ---
with tabs[1]:
    st.subheader("Stel een vraag aan de MCP Agent")
    mcp_query = st.text_input("Vraag van centralist/hulpverlener", placeholder="Bijv. De melder is vertrokken — wat nu?")
    if mcp_query and user_input:
        try:
            response = requests.post("http://localhost:8000/query", json={
                "query": mcp_query,
                "context": user_input
            })
            st.markdown(f"**🧠 Antwoord van de MCP Agent:** {response.json()['response']}")
        except Exception as e:
            st.error(f"Kan geen verbinding maken met de MCP Agent. Draait de server lokaal? Fout: {e}")

# --- TAB 3: Incidentkaart ---
with tabs[2]:
    if user_input:
        st.subheader("📋 Printbare Incidentkaart")
        html_card = generate_incident_card(user_input)
        st.components.v1.html(html_card, height=500, scrolling=True)

# --- TAB 4: Sentiment & Risico ---
with tabs[3]:
    if user_input:
        st.subheader("💬 Sentiment Analyse")
        sentiment, emotions = sentiment_analysis(user_input)
        st.info(f"📈 Dominant Sentiment: **{sentiment}**")
        st.markdown("📊 Emotie verdeling:")
        plot_sentiment_chart(sentiment)

        st.subheader("⚠️ Risicofactoren Visualisatie")
        plot_risk_factors(user_input)

# --- TAB 5: Admin - Hertrain Model ---
with tabs[4]:
    st.subheader("🔄 Hertrain gevaarmodel")
    st.markdown("Klik op de knop hieronder om het model opnieuw te trainen op basis van de laatste data in de database.")
    if st.button("Model hertrainen"):
        retrain_model_from_db()
        st.success("✅ Model succesvol hertraind en opgeslagen als danger_score_model.pkl.")

