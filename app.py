import streamlit as st
import pandas as pd
import requests

# Local modules
from model.scoring import score_transcript
from analysis.analyzer import run_sensitivity_analysis
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
from model.fallback import danger_score  # fallback if model fails

# App config
st.set_page_config(page_title="911 Danger Score Estimator", layout="wide")
st.title("📞 911 Danger Score Estimator")

st.markdown("""
This tool processes 911 call transcripts to estimate threat level using a trained ML model,
generate worst-case and branching scenarios, suggest next-best actions, and offer real-time MCP agent support.
""")

# Tabs for functionality
tabs = st.tabs(["📋 Transcript Analysis", "🧠 Ask the MCP Agent"])

# --- TAB 1: Transcript Analysis --- #
with tabs[0]:
    user_input = st.text_area("Paste a 911 call transcript below:", height=300)

    if user_input:
        try:
            score = score_transcript(user_input)
            st.success(f"🧠 ML-Based Danger Score: `{score:.2f}`")
        except Exception:
            score = danger_score(user_input)
            st.warning(f"⚠️ Using fallback (keyword-based) danger score: `{score:.2f}`")

        st.markdown("### ⚙️ Sensitivity Analysis")
        results = run_sensitivity_analysis(user_input)
        st.table(pd.DataFrame(results))

        st.markdown("### 🧾 Printable Incident Card")
        html_card = generate_incident_card(user_input)
        st.components.v1.html(html_card, height=800, scrolling=True)

        if st.button("📄 Download Incident Card as HTML"):
            with open("incident_card.html", "w") as f:
                f.write(html_card)
            st.success("✅ Incident card saved as HTML. You may print or convert to PDF.")

        st.markdown("### 📉 Sentiment & Emotion Analysis")
        sentiment_df = sentiment_analysis(user_input)
        plot_sentiment_chart(sentiment_df)
        st.dataframe(sentiment_df)

        st.markdown("### 🧱 Risk Factor Breakdown")
        plot_risk_factors(user_input)

# --- TAB 2: MCP Agent Interface --- #
with tabs[1]:
    st.markdown("Ask a question based on the current 911 incident.")
    mcp_query = st.text_input("Dispatcher/MCP Question", placeholder="e.g. Caller fled before arrival — what now?")
    if mcp_query and user_input:
        try:
            response = requests.post("http://localhost:8000/query", json={
                "query": mcp_query,
                "context": user_input
            })
            st.markdown(f"**🧠 MCP Agent Response:** {response.json()['response']}")
        except Exception as e:
            st.error(f"Failed to connect to MCP Agent. Is it running locally? Error: {e}")
