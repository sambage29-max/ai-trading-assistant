import streamlit as st
import requests

# --- CONFIGURATION ---
API_KEY = "271254f3-895f-4e4d-adc2-52146b6686c1"
API_SECRET = "yqo95s1v6n"
redirect_uri = "http://localhost:8501/"

st.title("🚀 Personal AI Trading Dashboard")

# --- AUTHENTICATION FLOW ---
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if not st.session_state.access_token:
    st.write("### 🔥 STEP 1: LOGIN TO UPSTOX")
    
    # FIX: Correct direct authentication link
    auth_url = f"https://upstox.com{API_KEY}&redirect_uri={redirect_uri}"
    
    st.markdown(f"👉 **[CLICK HERE TO LOGIN & AUTHORIZE APP]({auth_url})**")
    st.markdown("---")
    
    st.write("### 🔑 STEP 2: ENTER CODE TO ACTIVATE ENGINE")
    auth_code = st.text_input("Enter Authorization Code:", key="auth_code_input")
    
    if st.button("Generate Access Token"):
        if auth_code:
            # FIX: Correct token API endpoint
            token_url = "https://upstox.com"
            
            payload = {
                'code': auth_code,
                'client_id': API_KEY,
                'client_secret': API_SECRET,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            try:
                response = requests.post(token_url, data=payload, headers=headers)
                json_response = response.json()
                
                if "access_token" in json_response:
                    st.session_state.access_token = json_response["access_token"]
                    st.success("✅ Access Token active hogaya hai!")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {json_response.get('errors', [{}])[0].get('message', 'Unknown Error')}")
            except Exception as e:
                st.error(f"❌ Connection Error: {str(e)}")
        else:
            st.error("⚠️ code daalna zaroori hai!")
else:
    st.success("🎉 Engine Running Successfully!")
    st.write(f"Token: `{st.session_state.access_token[:10]}...*hidden*`")
    if st.button("Logout"):
        st.session_state.access_token = None
        st.rerun()
