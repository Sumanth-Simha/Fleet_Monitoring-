import streamlit as st
from utils.session import init_session

init_session()

st.set_page_config(page_title="Fleet Dashboard")

st.title("🚗 Fleet Risk Intelligence Dashboard")