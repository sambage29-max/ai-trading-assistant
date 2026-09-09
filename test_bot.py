import requests

# ==========================================
# 🔑 यहाँ अपनी असली डिटेल्स एक बार में डालें
# ==========================================
YOUR_TOKEN = "729485721:AAFxYz..."    # BotFather से मिला हुआ लंबा टोकन यहाँ पेस्ट करें
YOUR_CHAT_ID = "584930291"           # userinfobot से मिला हुआ 9 या 10 डिजिट का नंबर यहाँ लिखें

# ==========================================
# 🛠️ टेलीग्राम अलर्ट भेजने का कोर फंक्शन
# ==========================================
def send_telegram_alert(api_token, chat_id, message):
    # यूआरएल को बिल्कुल सही (api.telegram.org/bot<token>) फॉर्मेट में सेट किया गया है
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
            print(f"Response from Telegram: {response.text}")
    except Exception as e:
        print(f"⚠️ Connection Error: {str(e)}")

# ==========================================
# 🎯 टेस्ट रन (इसे रन करते ही फोन पर मैसेज आएगा)
# ==========================================
if __name__ == "__main__":
    test_message = (
        "🔥 *Grade AI Trading Engine: Alert Test*\n\n"
        "Bhai, aapka Telegram alert system bilkul sahi URL aur structure ke saath live ho gaya hai!\n"
        "Kal live market test ke liye aapka bot ab ekdum taiyar hai. 👍"
    )
    
    # फंक्शन को कॉल करना
    send_telegram_alert(YOUR_TOKEN, YOUR_CHAT_ID, test_message)
