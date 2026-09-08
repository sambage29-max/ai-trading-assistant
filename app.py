from datetime import datetime
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI Trading System", layout="wide")
st.title("🚀 Personal AI Trading Dashboard")

# --- STRICT HARDCODING FOR MOBILE AUTH FIX ---
# Bhai yahan apni asli credentials copy-paste kar do
API_KEY = "271254f3-895f-4e4d-adc2-52146b6686c1" 
API_SECRET = "yqo95s1v6n"
REDIRECT_URI = "https://google.com"

if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Purely hardcoded strict URL bypass mechanism
if API_KEY and API_KEY != "YOUR_API_KEY_HERE":
    base_url = "https://upstox.com"
    auth_url = f"{base_url}?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"
    
    st.markdown("### 🔥 STEP 1: LOGIN TO UPSTOX")
    st.markdown(f"## [👉 CLICK HERE TO LOGIN & AUTHORIZE APP]({auth_url})")
else:
    st.warning("Bhai pehle app.py me apni real API Key paste karke file save karo!")

st.markdown("---")
st.subheader("🔑 STEP 2: ENTER CODE TO ACTIVATE ENGINE")
auth_code = st.text_input("Enter Authorization Code:")

if st.button("Generate Access Token") and auth_code:
    token_url = "https://upstox.com"
    payload = {
        'code': auth_code, 'client_id': API_KEY, 'client_secret': API_SECRET,
        'redirect_uri': REDIRECT_URI, 'grant_type': 'authorization_code'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
    
    response = requests.post(token_url, data=payload, headers=headers)
    if response.status_code == 200:
        st.session_state.access_token = response.json().get('access_token')
        st.success("🎉 Access Token Successfully Connected!")
    else:
        st.error(f"Error status: {response.text}")
