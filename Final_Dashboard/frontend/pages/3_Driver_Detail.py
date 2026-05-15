import streamlit as st
import pandas as pd
from utils.db import get_connection

if "selected_driver" not in st.session_state or not st.session_state.selected_driver:
    st.warning("Select a driver first")
    st.stop()

conn = get_connection()
driver_id = st.session_state.selected_driver

st.title(f"Driver {driver_id} Details")

df = pd.read_sql(
    f"SELECT * FROM driver_data WHERE driver_id='{driver_id}'",
    conn
)

st.dataframe(df)

if st.button("Inspect Driver"):
    st.session_state.inspect_mode = True