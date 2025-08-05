import streamlit as st
import requests
from model.scoring import score_transcript
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
from model.training import retrain_model_from_db

st.set_page_config(page_title="112 Incident Analyzer", layout="wide")

st.title("📞 112 Incident Analyzer (Nederland)")
st.markdown("Analyseer een 112-oproep om risico's in te schatten, emoties te detecteren en een incidentkaart te genereren.")

# --- TABS ---
tabs = st.tabs([
    "📞 Invoer & Analyse", 
    "💬 Sentiment & Risico’s", 
    "📝 Incidentkaart", 
    "🤖 MCP Agent", 
    "⚙️ Beheer"
])

# Global storage for analysis (shared across tabs)
if "last_transcript" not in st.session_state:
    st.session_state["last_transcript"] = ""
    st.session_state["last_score"] = 0.0
    st.session_state["last_analysis"] = []
    st.session_state["last_sentiment"] = ""
    st.session_state["last_emotions"] = []

# --- TAB 1: Transcript Invoer + Analyse ---
with tabs[0]:
    st.subheader("Voer transcript in van 112-oproep")
    user_input = st.text_area("Transcript", value=st.session_state["last_transcript"], height=300)

    if st.button("🔍 Analyseer"):
        st.session_state["last_transcript"] = user_input
        score = score_transcript(user_input)
        st.session_state["last_score"] = score

        st.subheader("📊 Gevaar Score")
        st.metric("Gevaarscore", f"{score:.2f} / 1.00")

        st.subheader("🔬 Gevoeligheidsanalyse")
        results = run_sensitivity_analysis(user_input)
        st.session_state["last_analysis"] = results
        plot_sensitivity_chart(results)
        plot_risk_factors(results)

        st.subheader("💬 Sentiment & Emoties")
        sentiment, emotions = sentiment_analysis(user_input)
        st.session_state["last_sentiment"] = sentiment
        st.session_state["last_emotions"] = emotions
        st.write(f"📌 Sentiment: **{sentiment}**")
        st.write("📌 Herkende emoties:", ", ".join(emotions))
        plot_sentiment_chart(user_input)

# --- TAB 2: Sentiment + Risico's ---
with tabs[1]:
    st.subheader("💬 Sentiment & Risicofactoren")
    if st.session_state["last_transcript"]:
        st.write(f"📌 Sentiment: **{st.session_state['last_sentiment']}**")
        st.write("📌 Herkende emoties:", ", ".join(st.session_state["last_emotions"]))
        plot_sentiment_chart(st.session_state["last_transcript"])
        plot_risk_factors(st.session_state["last_analysis"])
    else:
        st.info("Voer eerst een transcript in via tab 1.")

# --- TAB 3: Incidentkaart ---
with tabs[2]:
    st.subheader("📝 Incidentkaart")
    if st.session_state["last_transcript"]:
        html_card = generate_incident_card(st.session_state["last_transcript"])
        st.components.v1.html(html_card, height=400, scrolling=True)
    else:
        st.info("Voer eerst een transcript in via tab 1.")

# --- TAB 4: MCP Agent Interface ---
with tabs[3]:
    st.subheader("🤖 Vraag advies aan MCP Agent")
    mcp_query = st.text_input("Stel een vraag", placeholder="Bijv. De melder is gevlucht bij aankomst — wat nu?")
    if mcp_query and st.session_state["last_transcript"]:
        try:
            response = requests.post("http://localhost:8000/query", json={
                "query": mcp_query,
                "context": st.session_state["last_transcript"]
            })
            st.markdown(f"**🧠 Antwoord van MCP Agent:** {response.json()['response']}")
        except Exception as e:
            st.error(f"❌ Verbinding met MCP Agent mislukt. Draait deze lokaal? Foutmelding: {e}")
    elif not st.session_state["last_transcript"]:
        st.info("Voer eerst een transcript in via tab 1.")

# --- TAB 5: Beheer Paneel ---
with tabs[4]:
    st.subheader("⚙️ Modelbeheer")
    st.markdown("Train het gevaarmodel opnieuw op basis van opgeslagen oproepen in de database.")

    if st.button("🔁 Hertrain model"):
        with st.spinner("Model wordt hertraind..."):
            try:
                n = retrain_model_from_db()
                st.success(f"✅ Model hertraind met {n} records.")
            except Exception as e:
                st.error(f"❌ Hertraining mislukt: {e}")
