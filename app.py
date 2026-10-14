
import streamlit as st

st.set_page_config(
    page_title="Text Annotation Workbench",
    page_icon="📝",
    layout="wide",
)

st.title("Text Annotation Workbench")

st.write(
    "An interactive demonstration of NLP text annotation "
    "and quality assurance."
)

st.info(
    "Our goal: annotate text consistently, explain labeling "
    "decisions, and validate annotation quality."
)

st.subheader("Annotation Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Samples", 0)
col2.metric("Completed", 0)
col3.metric("Needs Review", 0)

st.caption("Demo version 1.0 · English Sentiment Annotation")
