from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "roki12345"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route("/")
def home():
    return "Roki webhook is running! Messages subscribed!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403
    
    # POST - receive messages
    data = request.get_json()
    print(data)
    
    try:
        if data['object'] == 'whatsapp_business_account':
            for entry in data['entry']:
                for change in entry['changes']:
                    if 'messages' in change['value']:
                        messages = change['value']['messages']
                        for msg in messages:
                            from_number = msg['from']
                            msg_type = msg['type']
                            if msg_type == 'text':
                                text = msg['text']['body']
                                send_reply(from_number, f"Hello! You said: {text}\n\nRoki Digital Hub bot is LIVE! 🚀")
    except Exception as e:
        print(f"Error: {e}")
    
    return "ok", 200

def send_reply(to, text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("Missing WHATSAPP_TOKEN or PHONE_NUMBER_ID")
        return
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    r = requests.post(url, headers=headers, json=data)
    print(r.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
