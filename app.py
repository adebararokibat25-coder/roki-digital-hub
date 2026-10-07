from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "roki12345"

@app.route("/")
def home():
    return "Roki webhook is running!"

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("New WhatsApp message:", data)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
