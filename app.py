from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import ta
import plotly.graph_objects as go

st.set_page_config(page_title="AI Trading System", layout="wide")
st.title("🚀 Personal AI Trading Dashboard")

st.sidebar.header("🔑 Upstox Credentials")
API_KEY = st.sidebar.text_input("Enter API Key:", type="password")
API_SECRET = st.sidebar.text_input("Enter API Secret:", type="password")
REDIRECT_URI = st.sidebar.text_input("Redirect URI:", value="https://google.com")

if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Exact Fix: Clean framework structured URL definition for Upstox API v2
if API_KEY and REDIRECT_URI:
    base_url = "https://upstox.com"
    auth_url = f"{base_url}?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"
    st.sidebar.markdown(f"### [🔗 Click here to Login & Authorize App]({auth_url})")

st.subheader("STEP 1: Log in and Authorize")
st.write("1. Upar sidebar mein credentials daal kar link par click karein.")
st.write("2. Upstox page khulne par OTP se login karein.")
st.write("3. Google standard page par redirect hone par URL se `code=` ke aage ka text copy karke yahan paste karein:")

auth_code = st.text_input("Enter Authorization Code:")

if st.button("Generate Access Token") and auth_code:
    token_url = "https://upstox.com"
    payload = {
        'code': auth_code,
        'client_id': API_KEY,
        'client_secret': API_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    
    response = requests.post(token_url, data=payload, headers=headers)
    if response.status_code == 200:
        st.session_state.access_token = response.json().get('access_token')
        st.success("🎉 Access Token Successfully Connected!")
    else:
        st.error(f"Error status: {response.text}")

st.markdown("---")
st.subheader("🖥️ App System Feed")
col1, col2 = st.columns(2)
col1.metric("Market System Connection", "CONNECTED ✅" if st.session_state.access_token else "AUTHENTICATION REQUIRED ❌")
col2.metric("Automation Status", "Idle (Awaiting Token)")
