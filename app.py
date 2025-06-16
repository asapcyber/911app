import streamlit as st
import pandas as pd
from model.scoring import score_transcript
from model.fallback import danger_score
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card
import requests

st.set_page_config(page_title="911 Danger Score Estimator", layout="wide")

st.title("📞 911 Danger Score Estimator & MCP Assistant")
st.markdown("""
Analyze a 911 call transcript to assess danger levels, simulate response outcomes, and consult the AI MCP agent for tactical advice.
""")

user_input = st.text_area("Paste a 911 call transcript below:", height=300)

if user_input:
    tabs = st.tabs([
        "🔍 Danger Analysis",
        "🤖 MCP Agent",
        "🧾 Incident Card",
        "📉 Sentiment & Risk"
    ])

    # --- TAB 1: Danger Score ---
    with tabs[0]:
        st.markdown("## 🔎 ML-Based Danger Score")
        try:
            score = score_transcript(user_input)
        except Exception as e:
            score = danger_score(user_input)
            st.warning(f"Using fallback (keyword-based) danger score: {score:.2f}")

        st.metric(label="Estimated Danger Score", value=f"{score:.2f}")

        st.markdown("## ⚙️ Sensitivity Analysis")
        results = run_sensitivity_analysis(user_input)
        st.table(pd.DataFrame(results))
        plot_sensitivity_chart(results)

    # --- TAB 2: MCP Agent Interface ---
    with tabs[1]:
        st.markdown("## 🤖 Ask MCP Agent for Guidance")
        mcp_query = st.text_input("Dispatcher/MCP Question", placeholder="e.g. Caller fled before arrival — what now?")
        if mcp_query:
            try:
                response = requests.post("http://localhost:8000/query", json={
                    "query": mcp_query,
                    "context": user_input
                })
                st.markdown(f"**🧠 MCP Agent Response:** {response.json()['response']}")
            except Exception as e:
                st.error(f"Failed to connect to MCP Agent. Is it running locally? Error: {e}")

    # --- TAB 3: Incident Card ---
    with tabs[2]:
        st.markdown("## 🧾 Printable Incident Card")
        html_card = generate_incident_card(user_input)
        st.components.v1.html(html_card, height=800, scrolling=True)

        if st.button("📄 Download Incident Card as HTML"):
            with open("incident_card.html", "w") as f:
                f.write(html_card)
            st.success("Incident card saved as HTML. You can convert it to PDF.")

    # --- TAB 4: Sentiment & Risk ---
    with tabs[3]:
        st.markdown("## 📉 Sentiment & Emotion Analysis")
        sentiment_df = sentiment_analysis(user_input)
        plot_sentiment_chart(sentiment_df)
        st.dataframe(sentiment_df)

        st.markdown("## 🧱 Risk Factor Breakdown")
        plot_risk_factors(user_input)
