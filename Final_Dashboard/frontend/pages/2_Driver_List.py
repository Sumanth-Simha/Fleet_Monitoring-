import streamlit as st
import pandas as pd
from utils.db import get_connection

if not st.session_state.logged_in:
    st.warning("Login first")
    st.stop()

conn = get_connection()

df = pd.read_sql("SELECT driver_id, vehicle_id FROM drivers;", conn)

st.title("Driver List")

for _, row in df.iterrows():
    col1, col2, col3 = st.columns([2,2,1])

    col1.write(row["driver_id"])
    col2.write(row["vehicle_id"])

    if col3.button("Inspect", key=row["driver_id"]):
        st.session_state.selected_driver = row["driver_id"]