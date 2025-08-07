# app.py

import streamlit as st
from model.scoring import score_transcript
from analysis.analyzer import run_sensitivity_analysis, plot_sensitivity_chart

st.set_page_config(page_title="112 Gevaar Analyse", layout="wide")

st.title("🚨 112 Transcript Analyse")
st.markdown("Voer hieronder een transcript in van een 112-noodgeval om het **gevaar niveau** en de **gevoelige termen** te analyseren.")

# --- Transcript Input ---
user_input = st.text_area("Transcript van 112-oproep (in het Nederlands)", height=200, placeholder="Bijv. 'Mijn vriend schreeuwt en bedreigt mij met een mes...'")

if user_input:
    # --- Danger Score ---
    score = score_transcript(user_input)
    st.markdown(f"### 🔥 Gevaarscore: `{score:.2f}`")
    st.markdown("_(0 = Laag risico, 1 = Hoog risico)_")

    # --- Sensitivity Analysis ---
    with st.spinner("Analyse van gevoelige termen..."):
        sensitivity_results = run_sensitivity_analysis(user_input)

    if sensitivity_results:
        st.markdown("### 🧠 Gevoeligheidsanalyse")
        fig = plot_sensitivity_chart(sensitivity_results)
        st.pyplot(fig)
    else:
        st.warning("Geen gevoelige termen geïdentificeerd.")
