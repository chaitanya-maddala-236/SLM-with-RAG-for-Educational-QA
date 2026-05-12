from __future__ import annotations

import asyncio

import streamlit as st

from project.app.models.schemas import UserInput
from project.app.rag.pipeline import EduSLMRAGPipeline

st.set_page_config(page_title="EduSLM-RAG", layout="wide")
st.title("EduSLM-RAG: Small-Model Educational QA")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = EduSLMRAGPipeline()
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.subheader("Filters")
    subject = st.text_input("Subject", value="science")
    grade = st.text_input("Grade", value="9")
    topic = st.text_input("Topic", value="general")

question = st.text_area("Ask a question")

if st.button("Generate Answer") and question.strip():
    payload = UserInput(
        question=question,
        chat_history=st.session_state.history,
        metadata_filters={"subject": subject, "grade": grade, "topic": topic},
    )
    result = asyncio.run(st.session_state.pipeline.run(payload))

    st.session_state.history.append({"role": "user", "content": question})
    st.session_state.history.append({"role": "assistant", "content": result.answer})

    st.subheader("Answer")
    st.write(result.answer)

    st.subheader("Citations")
    st.write(result.diagnostics.citations)

    st.subheader("Diagnostics")
    st.json({
        "retrieval_confidence": result.diagnostics.retrieval_confidence,
        "fallback_level": result.diagnostics.fallback_level,
        "ambiguity_detected": result.diagnostics.ambiguity_detected,
    })
