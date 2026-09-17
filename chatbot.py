import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
GRAPH = "https://graph.facebook.com/v25.0"

def send_message(phone_number, message):
    r = requests.post(f"{GRAPH}/{PHONE_NUMBER_ID}/messages",
                      headers={"Authorization": f"Bearer {TOKEN}"},
                      json={"messaging_product": "whatsapp", "to": phone_number,
                            "type": "text", "text": {"body": message}},
                            timeout=15)
    if not r.ok:
        print("send failed":, r.status_code, r.message)
    
    
app = Flask(__name__)

@app.get("/webhook")
def verify():
    body = request.args.get_json(silent=True)
    try:
        msg = body["entry"][0]["changes"][0]["value"]["messages"][0]
    except (KeyError, IndexError, TypeError):
        return "ok", 200
    
    if msg["type"] == "text":
        send_message(msg["from"], "You said: " + msg["text"]["body"])
    return "ok", 200

if __name__ == "__main":
    app.run(host="0.0.0.0", port=5000)