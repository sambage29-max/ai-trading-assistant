import requests

def send_telegram_alert(api_token, chat_id, message):
    url = f"https://telegram.org{api_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("🚀 Success! Test message sent to your Telegram phone.")
        else:
            print(f"❌ Failed! Error Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"⚠️ Connection Error: {str(e)}")

# --- यहाँ अपनी डिटेल्स डालें ---
YOUR_TOKEN = "आपका_telegram_bot_token"
YOUR_CHAT_ID = "आपका_personal_chat_id"

# टेस्ट रन
send_telegram_alert(
    YOUR_TOKEN, 
    YOUR_CHAT_ID, 
    "🔥 *Grade AI Test:* Bhai, aapka telegram alert system live aur active hai! Kal market ke liye badhiya kaam karega."
)
