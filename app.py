import streamlit as st
import requests

# --- CONFIGURATION (यहाँ अपनी डिटेल्स डालें) ---
# Upstox Developer Portal (://upstox.com) से कॉपी करके यहाँ पेस्ट करें
API_KEY = "271254f3-895f-4e4d-adc2-52146b6686c1"  
API_SECRET = "yqo95s1v6n"  

# ध्यान रहे: यह URL आपके Upstox Developer Portal पर सेट Redirect URL से अक्षर-टू-अक्षर मैच होना चाहिए
redirect_uri = "http://localhost:8501/"  

st.title("🚀 Personal AI Trading Dashboard")

# --- AUTHENTICATION FLOW ---
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if not st.session_state.access_token:
    st.write("### 🔥 STEP 1: LOGIN TO UPSTOX")
    
    if API_KEY and API_KEY != "YOUR_API_KEY_HERE":
        # बिल्कुल सही और फ्रेश Upstox v2 API ऑथेंटिकेशन URL
        auth_url = "https://upstox.com"


        
        st.markdown(f"👉 **[CLICK HERE TO LOGIN & AUTHORIZE APP]({auth_url})**")
    else:
        st.warning("⚠️ भाई, पहले कोड में सबसे ऊपर अपनी असली API Key (API_KEY) पेस्ट करके फाइल सेव करो!")

    st.markdown("---")
    
    st.write("### 🔑 STEP 2: ENTER CODE TO ACTIVATE ENGINE")
    auth_code = st.text_input("Enter Authorization Code (लॉगिन करने के बाद जो URL में code= मिला है, उसे यहाँ डालें):", key="auth_code_input")
    
    if st.button("Generate Access Token"):
        if auth_code and API_SECRET != "YOUR_API_SECRET_HERE":
            # Access Token जनरेट करने के लिए Upstox का सही API एंडपॉइंट
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
                    st.success("✅ Access Token सफलतापूर्वक जनरेट हो गया है! ट्रेडिंग इंजन एक्टिवेटेड है।")
                    st.rerun()
                else:
                    st.error(f"❌ टोकन जनरेट करने में एरर आया: {json_response.get('errors', [{}])[0].get('message', 'Unknown Error')}")
            except Exception as e:
                st.error(f"❌ कनेक्शन एरर: {str(e)}")
        else:
            st.error("⚠️ कृपया कोड बॉक्स में ऑथराइजेशन कोड डालें और सुनिश्चित करें कि आपने API Secret भी कोड में सेट कर दिया है।")

else:
    st.success("🎉 आप सफलतापूर्वक लॉग इन हैं! आपका AI ट्रेडिंग इंजन चालू है।")
    st.write(f"**आपका एक्टिव टोकन:** `{st.session_state.access_token[:10]}...*hidden*`")
    if st.button("Logout / Disconnect"):
        st.session_state.access_token = None
        st.rerun()
