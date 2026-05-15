import streamlit as st
from utils.session import init_session

init_session()

st.title("Inspector Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "1234":
        st.session_state.logged_in = True
        st.success("Logged in")
    else:
        st.error("Invalid credentials")