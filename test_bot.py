import requests

# ==========================================
# 🔑 Aapki Details Successfully Configured Hain
# ==========================================
YOUR_CHAT_ID = "7374819912"
YOUR_TOKEN = "8680517650:AAHYrpb5j88XNGIoK-xu-hC-qZWs3RtCHkk"

def send_telegram_alert(api_token, chat_id, message):
    # Fixed URL Structure
    url = f"https://telegram.org{api_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("🚀 Success! Test message sent to your Telegram phone.")
        else:
            print(f"❌ Failed! Error Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"⚠️ Connection Error: {str(e)}")

if __name__ == "__main__":
    test_message = (
        "🔥 *Grade AI Trading Engine: Alert Test*\n\n"
        "Bhai, aapka Telegram alert system bilkul sahi URL aur structure ke saath live ho gaya hai!\n"
        "Kal live market test ke liye aapka bot ab ekdum taiyar hai. 👍"
    )
    
    send_telegram_alert(YOUR_TOKEN, YOUR_CHAT_ID, test_message)
