import streamlit as st
import requests
ACCESS_TOKEN = st.secrets["UPSTOX_ACCESS_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈"
)

st.title("📈 AI Trading Assistant")

st.success("Step 1 Successful ✅")

st.write("Token loaded successfully ✅")
st.write(ACCESS_TOKEN[:10] + "...")
