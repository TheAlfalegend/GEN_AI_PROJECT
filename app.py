import os

import streamlit as st

from examples import EXAMPLES, explain_demo
from explainer import DEFAULT_MODEL, MAX_TOPIC, ExplainerError, clean_topic, explain_live

st.set_page_config(page_title="Concept Explainer · PS 23", page_icon="📘")

api_key = os.getenv("GEMINI_API_KEY", "").strip()
model = os.getenv("GEMINI_MODEL", "").strip() or DEFAULT_MODEL

st.caption("GENAI MINI PROJECT · PS 23")
st.title("Concept Explainer")
st.markdown("One topic, three explanations. Start with an analogy, learn how it works, then dig into the details.")

mode = st.radio("Explanation mode", ("Demo", "Live AI"), index=int(bool(api_key)), horizontal=True)
if mode == "Demo":
    st.caption("Offline demo · built-in examples, not AI-generated output.")
else:
    st.caption(f"Live mode · {model} · your concept is sent to Google Gemini.")
    if not api_key:
        st.info("Live AI needs a Gemini API key. See the README to set it locally; Demo works without a key.")


def use_example(example):
    st.session_state["concept"] = example


st.caption("Try an example")
for column, example in zip(st.columns(len(EXAMPLES)), EXAMPLES):
    column.button(example, on_click=use_example, args=(example,))

with st.form("concept_form"):
    topic = st.text_input("Concept", placeholder="e.g. Gravity", max_chars=MAX_TOPIC, key="concept")
    submitted = st.form_submit_button("Explain", type="primary")

if submitted:
    st.session_state.pop("result", None)
    try:
        topic = clean_topic(topic)
        if mode == "Demo":
            answers = explain_demo(topic)
        else:
            with st.spinner("Generating three explanations…"):
                answers = explain_live(topic, api_key, model)
        st.session_state["result"] = (mode, topic, answers)
    except ExplainerError as error:
        st.warning(str(error))

result = st.session_state.get("result")
if result and result[0] == mode:
    _, result_topic, answers = result
    st.divider()
    st.text(f"TOPIC: {result_topic}")
    for tab, level, subtitle in zip(
        st.tabs(["Kid", "Student", "Expert"]),
        ("kid", "student", "expert"),
        ("The basic idea", "How it works", "The technical details"),
    ):
        with tab:
            st.subheader(subtitle)
            st.text(answers[level])
    if mode == "Live AI":
        st.caption("AI-generated explanations may contain errors. Check important details against reliable sources.")
else:
    st.caption("Enter a concept or pick an example, then select Explain.")
