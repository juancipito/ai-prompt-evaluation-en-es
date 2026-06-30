from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_synthetic_data.csv"
SCORE_COLS = ["helpfulness", "accuracy", "safety", "clarity", "bilingual_quality"]

st.set_page_config(page_title="AI Prompt Evaluation EN/ES", layout="wide")
st.title("AI Prompt Evaluation EN/ES")
st.caption("Synthetic bilingual prompt-response evaluation dataset.")

df = pd.read_csv(DATA_PATH)
language = st.selectbox("Language", ["All"] + sorted(df["language"].unique()))
if language != "All":
    df = df[df["language"] == language]

st.metric("Average score", f"{df['overall_score'].mean():.2f}/5")
st.metric("Review rate", f"{(df['risk_flag'].eq('review').mean() * 100):.1f}%")
st.bar_chart(df[SCORE_COLS].mean())
st.dataframe(df[["prompt_id", "language", "category", "overall_score", "risk_flag", "evaluator_note"]], use_container_width=True)
