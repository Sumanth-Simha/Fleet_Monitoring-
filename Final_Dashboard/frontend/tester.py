import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
from streamlit_autorefresh import st_autorefresh

# ----------------------------
# ENV
# ----------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ----------------------------
# Auto refresh metrics
# ----------------------------
st_autorefresh(
    interval=2000,
    key="refresh"
)

st.title("🚗 Driver Monitoring Live Dashboard")

# ----------------------------
# VIDEO STREAM
# ----------------------------
st.subheader("Live Dashcam Feed")

video_url = "http://localhost:8000/video_feed"

st.image(video_url)

# ----------------------------
# LIVE METRICS
# ----------------------------
st.subheader("Live Driver Metrics")

try:
    response = supabase.table(
        "live_driver_state"
    ).select("*").eq(
        "id", 1
    ).execute()

    data = response.data[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("EAR", round(data["ear"], 3))
        st.metric("PERCLOS", round(data["perclos"], 3))
        st.metric("Blink Rate", data["blink_rate"])

    with col2:
        st.metric("Driver State", data["driver_state"])
        st.metric(
            "Fatigue Score",
            round(data["fatigue_score"], 3)
        )
        st.metric(
            "Eye Closure Duration",
            round(data["eye_closure_duration"], 3)
        )

except Exception as e:
    st.error(f"Error fetching metrics: {e}")