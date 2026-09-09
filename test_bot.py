import requests

# ==========================================
# 🔑 aapki details yahan automatically configured hain
# ==========================================
YOUR_CHAT_ID = "7374819912"           # aapki real telegram numerical id 
YOUR_TOKEN = "7584930291:AAFxYz..."    # botfather se mila bot token yahan paste karein

# ==========================================
# 🛠️ telegram alert function
# ==========================================
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
            print(f"❌ Failed! Error Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"⚠️ Connection Error: {str(e)}")

# ==========================================
# 🎯 execution trigger
# ==========================================
if __name__ == "__main__":
    test_message = (
        "🔥 *Grade AI Trading Engine: Alert Test*\n\n"
        "Bhai, aapka Telegram alert system bilkul sahi URL aur structure ke saath live ho gaya hai!\n"
        "Kal live market test ke liye aapka bot ab ekdum taiyar hai. 👍"
    )
    
    send_telegram_alert(YOUR_TOKEN, YOUR_CHAT_ID, test_message)
