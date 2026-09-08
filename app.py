from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import ta  # Aapki requirements file se technical indicators module
import plotly.graph_objects as go  # Charts draw karne ke liye

# Page Setup
st.set_page_config(page_title="AI Trading System", layout="wide")
st.title("🚀 Personal AI Trading Dashboard")

# Sidebar Configuration
st.sidebar.header("🔑 Upstox Credentials")
API_KEY = st.sidebar.text_input("Enter API Key:", type="password")
API_SECRET = st.sidebar.text_input("Enter API Secret:", type="password")
REDIRECT_URI = st.sidebar.text_input("Redirect URI:", value="https://google.com")

# Initialize Session Tokens
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Sahi URL Structure framework deploy karne ke liye
if API_KEY and REDIRECT_URI:
    # Upstox Official login workflow link
    auth_url = f"https://upstox.com{API_KEY}&redirect_uri={REDIRECT_URI}"
    st.sidebar.markdown(f"### [🔗 Click here to Login & Authorize App]({auth_url})")

# User Authentication Code Box
st.subheader("STEP 1: Log in and Authorize")
st.write("Upar sidebar mein link par click karke login karein, fir redirect hue URL se `code=` ke aage ka text yahan paste karein:")
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
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
    
    response = requests.post(token_url, data=payload, headers=headers)
    if response.status_code == 200:
        st.session_state.access_token = response.json().get('access_token')
        st.success("🎉 Access Token Successfully Connected!")
    else:
        st.error(f"Error: {response.text}")

# System Status metrics display
st.markdown("---")
st.subheader("🖥️ Live App Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Market Status", "CONNECTED ✅" if st.session_state.access_token else "AUTHENTICATION REQUIRED ❌")
col2.metric("Libraries Loaded", "ta, plotly, pandas")
col3.metric("System Engine", "Ready to fetch logs")
