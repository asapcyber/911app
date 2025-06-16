import os
import streamlit as st
import pandas as pd

from model.scoring import score_transcript
from model.fallback import danger_score as fallback_score
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart
from analysis.sentiment_module import sentiment_analysis, plot_sentiment_chart
from analysis.visuals import plot_risk_factors
from card.card_generator import generate_incident_card

# Set up Streamlit page
st.set_page_config(page_title="911 Danger Score Estimator")
st.title("📞 911 Danger Score Estimator")

st.markdown("""
Analyze 911 call transcripts using machine learning to assess potential threat levels.  
Includes dynamic risk scoring, sensitivity analysis, scenario planning, and emotion analysis.
""")

# Input field
user_input = st.text_area("📋 Paste a 911 call transcript below:", height=300)

if user_input:
    st.markdown("## 🔎 ML-Based Danger Score")
    score = score_transcript(user_input)
    st.metric(label="Estimated Danger Score", value=f"{score:.2f}", delta=None)

    # Sensitivity analysis
    st.markdown("---")
    st.markdown("## ⚙️ Sensitivity Analysis (ML-Based)")
    results = run_sensitivity_analysis(user_input)
    st.table(pd.DataFrame(results))
    plot_sensitivity_chart(results)

    # Incident card generation
    st.markdown("---")
    st.markdown("## 🧾 Printable Incident Card")
    html_card = generate_incident_card(user_input)
    st.components.v1.html(html_card, height=800, scrolling=True)

    if st.button("📄 Download Incident Card as HTML"):
        with open("incident_card.html", "w") as f:
            f.write(html_card)
        st.success("Incident card saved as HTML. You can convert this to PDF using your browser or wkhtmltopdf.")

    # Sentiment + emotion analysis
    st.markdown("---")
    st.markdown("## 📉 Sentiment & Emotion Analysis")
    sentiment_df = sentiment_analysis(user_input)
    plot_sentiment_chart(sentiment_df)
    st.dataframe(sentiment_df)

    # Risk factor contribution chart
    st.markdown("---")
    st.markdown("## 🧱 Risk Factor Breakdown")
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
