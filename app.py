# app.py
import streamlit as st
from model.scoring import score_transcript
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart, extract_dutch_keywords
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
from model.training import retrain_model_from_db

st.set_page_config(page_title="112 Gevaar Analyse", layout="wide")
st.title("🚨 112 Gevaar Analyse en Incident Assistentie")

# --- UI Tabs --- #
tabs = st.tabs(["📋 Incident Kaart", "📊 Sentiment & Risico", "⚙️ Admin Panel"])

# === 📋 TAB 1: Incident Kaart === #
with tabs[0]:
    st.subheader("Transcript invoer (in het Nederlands)")
    user_input = st.text_area("Plak hier het transcript van het 112-gesprek", height=300)

    if user_input:
        score = score_transcript(user_input)
        st.markdown(f"### 🧠 Gevaar Score: `{score:.2f}` (0 = Laag risico, 1 = Hoog risico)`")

        # --- Sensitivity Analysis --- #
        st.markdown("### 🔍 Gevoeligheidsanalyse")
        results = run_sensitivity_analysis(user_input)
        if results:
            st.markdown("**Top gevoelige termen:**")
            st.write([r["Scenario"] for r in results])
            plot_sensitivity_chart(results)
        else:
            st.info("Geen gevoelige termen gedetecteerd.")

        # --- Incident Card --- #
        st.markdown("### 🧾 Incident Kaart")
        html_card = generate_incident_card(user_input)
        st.components.v1.html(html_card, height=800, scrolling=True)

# === 📊 TAB 2: Sentiment & Risico === #
with tabs[1]:
    if user_input:
        st.subheader("📉 Sentiment- en Emotieanalyse")
        sentiment_df, emotion_df = sentiment_analysis(user_input)
        st.dataframe(sentiment_df)
        plot_sentiment_chart(sentiment_df)

        st.subheader("📊 Risicofactor Visualisatie")
        plot_risk_factors(user_input)

# === ⚙️ TAB 3: Admin Panel === #
with tabs[2]:
    st.subheader("🔁 Model Hertrainen")
    if st.button("🎯 Hertrain model met huidige database"):
        retrain_model_from_db()
        st.success("Model succesvol hertraind en opgeslagen als .pkl bestand.")

    st.subheader("🔑 Debug: Trefwoorden uit huidige transcript")
    if user_input:
        keywords = extract_dutch_keywords(user_input)
        st.write("🔎 Gedetecteerde sleutelwoorden:", keywords)

# === 🤖 TAB 4: MCP Agent Assistentie === #
tabs.append(st.container())  # Add a new container for the 4th tab

with st.expander("🤖 MCP Agent Assistentie (Dispatcher hulp via AI)", expanded=True):
    st.markdown("Typ hier een vraag over de huidige 112-melding. De AI-agent zal adviseren op basis van het transcript.")

    mcp_query = st.text_input("🧠 Vraag voor MCP Agent", placeholder="Bijv. Hulpdiensten arriveren maar de melder is gevlucht — wat nu?")
    
    if mcp_query and user_input:
        import requests
        try:
            response = requests.post("http://localhost:8000/query", json={
                "query": mcp_query,
                "context": user_input
            })
            if response.status_code == 200:
                st.markdown(f"**🧠 Antwoord van MCP Agent:** {response.json()['response']}")
            else:
                st.error("⚠️ Geen antwoord ontvangen van de MCP server.")
        except Exception as e:
            st.error(f"❌ Fout bij verbinden met MCP Agent: {e}")
