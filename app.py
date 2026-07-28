import streamlit as st
import requests

st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈"
)

ACCESS_TOKEN = st.secrets["UPSTOX_ACCESS_TOKEN"]

st.title("📈 AI Trading Assistant")
st.success("Step 1 Complete ✅")
