import streamlit as st
import requests
ACCESS_TOKEN = "TEST"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈"
)

st.title("📈 AI Trading Assistant")

st.success("Step 1 Successful ✅")
