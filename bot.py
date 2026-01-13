import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration - Heroku पर environment variables से लेंगे
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN')
VERCEL_URL = os.environ.get('VERCEL_URL', 'https://your-vercel-app.vercel.app')
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# --- FUNCTION TO SEND REQUESTS TO TELEGRAM ---
def send_request(method, params):
    """Telegram API को request भेजने के लिए function"""
    url = API_URL + method
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Telegram API Error ({method}): {e}")
        return None

# --- WEBHOOK ENDPOINT ---
@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram से updates प्राप्त करने के लिए webhook endpoint"""
    update = request.json
    
    if not update:
        return jsonify({"status": "no data"}), 400
    
    # Handle /start command
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text.startswith('/start'):
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🎶 Open free course 🎶",
                            "web_app": {"url": VERCEL_URL}
                        }
                    ]
                ]
            }
            
            params = {
                "chat_id": chat_id,
                "text": "Click the button below to launch the your favourite course!",
                "reply_markup": keyboard
            }
            
            send_request("sendMessage", params)
    
    return jsonify({"status": "ok"}), 200

# --- SET WEBHOOK (एक बार run करने के लिए) ---
@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    """Telegram bot के लिए webhook set करें"""
    webhook_url = f"https://{request.host}/webhook"
    params = {"url": webhook_url}
    
    result = send_request("setWebhook", params)
    
    if result and result.get('ok'):
        return f"Webhook set successfully to: {webhook_url}"
    else:
        return f"Failed to set webhook: {result}"

# --- ROOT ENDPOINT ---
@app.route('/')
def index():
    return "Telegram Bot is running!"

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
