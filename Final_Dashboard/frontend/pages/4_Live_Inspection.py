import streamlit as st

if "inspect_mode" not in st.session_state or not st.session_state.inspect_mode:
    st.warning("Start inspection first")
    st.stop()

st.title("Live Inspection")

st.image("http://localhost:8000/video_feed")