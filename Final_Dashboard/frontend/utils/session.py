import streamlit as st

def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "selected_driver" not in st.session_state:
        st.session_state.selected_driver = None

    if "inspect_mode" not in st.session_state:
        st.session_state.inspect_mode = False