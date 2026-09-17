import sqlite3
import time
from lessons import LESSONS, VIDEOS
import re
import ollama
import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
GRAPH = "https://graph.facebook.com/v25.0"
DB_PATH = "pypaper.db"
MAXIMUM_ATTEMPTS = 3

def init_database():
    with database() as c:
        c.executescript("""CREATE TABLE IF NOT EXISTS students (
                                phone TEXT PRIMARY KEY,
                                current_lesson INTEGER NOT NULL DEFAULT 1,
                                current_step INTEGER NOT NULL DEFAULT 0,
                                attempts INTEGER NOT NULL DEFAULT 0,
                                score INTEGER NOT NULL DEFAULT 0);
                            CREATE TABLE IF NOT EXISTS events (phone TEXT, event TEXT, detail TEXT, ts REAL);
                            CREATE TABLE IF NOT EXISTS seen_messages (id TEXT PRIMARY KEY, ts REAL);""")

def database():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def get_student(phone):
    with database() as c:
        row = c. execute("SELECT * FROM students WHERE phone = ?", (phone,)).fetchone()
        return dict(row) if row else None
    
def create_student(phone):
    with database() as c:
        c.execute("INSERT INTO students (phone) VALUES (?)", (phone,))
    log_event(phone, "enrolled")
    return get_student(phone)

def update_student(phone, **fields):
    sets = ", ".join(f"{k} = ?" for k in fields)
    with database() as c:
        c.execute(f"UPDATE students SET {sets} WHERE phone = ?", (*fields.values(), phone))

def log_event(phone, event, detail=None):
    with database() as c:
        c.execute("INSERT INTO events VALUES (?, ?, ?, ?)", (phone, event, detail, time.time()))

def already_seen(message_id):
    with database() as c:
        try:
            c.execute("INSERT INTO seen_messages VALUES (?, ?)", (message_id, time.time()))
            return False
        except sqlite3.IntegrityError:
            return True

def send_message(phone_number, message):
    r = requests.post(f"{GRAPH}/{PHONE_NUMBER_ID}/messages",
                      headers={"Authorization": f"Bearer {TOKEN}"},
                      json={"messaging_product": "whatsapp", "to": phone_number,
                            "type": "text", "text": {"body": message}},
                            timeout=15)
    if not r.ok:
        print("send failed", r.status_code, r.text)
    
def download_media(media_id):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    info = requests.get(f"{GRAPH}/{media_id}", headers=headers, timeout=15).json()
    img = requests.get(info["url"], headers=headers, timeout=30)
    return img.content, info.get("mime_type", "image/jpeg")

OLLAMA_MODEL = "gemma3:4b"
TRANSCRIBE_PROMPT = """This photo shows a short Python program handwritten on paper by a beginner.
Copy out exactly what is written, line by line, as plain text.
DO NOT FIX MISTAKES. DO NOT ADD MISSING LINES. DO NOT EXPLAIN.
If a character is not clear, just guess.
Reply with code only"""

def transcribe_photo(image_bytes):
    response = ollama.chat(
        model = OLLAMA_MODEL,
        messages=[{"role": "user", "content": TRANSCRIBE_PROMPT, "images": [image_bytes]}],
        options={"temperature": 0}
    )
    code = response["message"]["content"].strip()
    code = re.sub(r"^```(?:python)?\s*|\s*```$", "", code)
    return code.strip()


app = Flask(__name__)

@app.get("/webhook")
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge", ""), 200
    return "wrong verify token", 403

@app.post("/webhook")
def recieve():
    body = request.get_json(silent=True)
    try:
        msg = body["entry"][0]["changes"][0]["value"]["messages"][0]
    except (KeyError, IndexError, TypeError):
        return "ok", 200
    
    if msg["type"] == "text":
        send_message(msg["from"], "You said: " + msg["text"]["body"])
    elif msg["type"] == "image":
        image, mime = download_media(msg["image"]["id"])
        code = transcribe_photo(image)
        patterns = [r"for\s*\w+\s+in\s+range\s*\(\s*3\s*\)\s*:", r"print\s*\(\s*[\"']#[\"']\s*\)"]
        ok = all(re.search(p, code, re.IGNORECASE) for p in patterns)
        send_message(msg["from"], f"I read:\n\n{code}\n\n" + ("Correct!" if ok else "Not quite yet"))
    return "ok", 200

init_database()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
