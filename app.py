import streamlit as st
import requests

from model.scoring import score_transcript
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
from model.training import retrain_model_from_db

st.set_page_config(page_title="112 Incident Analyzer", layout="wide")
st.title("112 Incident Analyzer 🇳🇱")
st.markdown("Voer een transcript van een 112-melding in en analyseer de risico's, emoties en aanbevelingen.")

# --- Input transcript field
user_input = st.text_area("📋 Transcript invoeren (in het Nederlands)", height=300)

# --- Tabs setup
tabs = st.tabs(["📑 Incidentkaart", "📊 Sentiment & Risicoanalyse", "🛠️ Beheer", "🤖 MCP Agent"])

# --- Tab 1: Incident Card
with tabs[0]:
    if user_input:
        st.subheader("🔍 Gevaarscore en Analyse")
        score = score_transcript(user_input)
        st.markdown(f"**Gevaar Score:** {score:.2f} (0 = Laag risico, 1 = Hoog risico)")

        results = run_sensitivity_analysis(user_input)
        html_card = generate_incident_card(user_input)
        st.markdown(html_card, unsafe_allow_html=True)

# --- Tab 2: Sentiment & Risk
with tabs[1]:
    if user_input:
        st.subheader("📈 Emotionele Analyse en Risicofactoren")

        # --- Sentiment
        sentiment, emotion_df = sentiment_analysis(user_input)
        fig1 = plot_sentiment_chart(emotion_df)
        if fig1:
            st.pyplot(fig1)

        # --- Risk Factors
        fig2 = plot_risk_factors(user_input)
        if fig2:
            st.pyplot(fig2)

        # --- Data Table
        st.write("**Gedetecteerde emoties en sentimenten:**")
        st.dataframe(emotion_df)


# --- Tab 3: Admin Panel
with tabs[2]:
    st.subheader("🔄 Model opnieuw trainen")
    st.markdown("Klik op de onderstaande knop om het ML-model opnieuw te trainen op basis van de laatste gegevens in de database.")
    if st.button("📚 Start Hertraining"):
        retrain_model_from_db()
        st.success("✅ Model opnieuw getraind en opgeslagen!")

# --- Tab 4: MCP Agent
with tabs[3]:
    st.subheader("💬 Vraag de MCP Agent")
    mcp_query = st.text_input("Stel een vraag op basis van het incident", placeholder="Bijv. De melder is gevlucht — wat nu?")
    if mcp_query and user_input:
        try:
            response = requests.post("http://localhost:8000/query", json={
                "query": mcp_query,
                "context": user_input
            })
            st.markdown(f"**🧠 Antwoord van de MCP Agent:** {response.json()['response']}")
        except Exception as e:
            st.error(f"Verbinding met MCP Agent mislukt. Draait de server lokaal? Foutmelding: {e}")
