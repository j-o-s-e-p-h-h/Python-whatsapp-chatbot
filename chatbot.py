import sqlite3
import time
import threading
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

WELCOME = ("Welcome to Pypaper! Learn Python with just a pen and paper. \n"
           "The lessons follow Harvard's free CS50P course.\n\n"
           "Never write your name on pages you photograph.\n\n"
           "Type HELP anytime you feel lost or want commands. Type START to begin!")

HELP = ("Commands:\n"
        "START - begin or continue\n"
        "PROGrESS - see your score\n"
        "RESTART - start the current lesson again\n"
        "HELP - this message\n\n"
        "Otherwise just answer the question.")

def normalise(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def current_step(student):
    steps = LESSONS[student["current_lesson"]]["steps"]
    i = student["current_step"]
    return steps[i] if i < len(steps) else None

def handle_message(message):
    phone = message["from"]
    student = get_student(phone)

    if student is None:
        student = create_student(phone)
        send_message(phone, WELCOME)
        present(phone, student)
        return
    
    if message["kind"] == "image":
        handle_image(phone, student, message["media_id"])
        return
    
    cmd = normalise(message["text"] or "").upper()
    step = current_step(student)
    if cmd == "HELP":
        send_message(phone, HELP)
    elif cmd == "PROGRESS":
        send_message(phone, f"📊 Lesson {student['current_lesson']}, "
                            f"step {student['current_step'] + 1}. Score: {student['score']} ⭐")
    elif cmd == "RESTART":
        update_student(phone, current_step=0, attempts=0)
        present(phone, get_student(phone))
    elif cmd == "START" or step is None or step["type"] in ("teach", "video"):
        present(phone, student)               
    else:
        check_answer(phone, student, step, message["text"])

def present(phone, student):
    while True:
        step = current_step(student)
        if step is None:
            finish_lesson(phone, student)
            return
        if step["type"] == "choice":
            send_buttons(phone, step["text"], step["options"])
            return
        if step["type"] == "video":
            video = VIDEOS[step["video"]]
            send_message(phone, f"{step["text"]}\n\n📺{video['title']}\n{video['url']}")
        else:
            send_message(phone, step["text"])
        if step["type"] not in ("teach", "video"):
            return
        
        student = advance(phone, student)

def advance(phone, student):
    update_student(phone, current_step=student["current_step"] + 1, attempts=0)
    return get_student(phone)
    
def finish_lesson(phone, student):
    lesson = student["current_lesson"]
    log_event(phone, "lesson_completed", str(lesson))
    if lesson + 1 in LESSONS:
        update_student(phone, current_lesson=lesson + 1, current_step=0, attempts=0)
        send_message(phone, f"Lesson {lesson} complete! Score: {student['score']}")

def send_buttons(phone_number, text, options):
    buttons = [{"type": "reply", "reply": {"id": i, "title": t[:20]}} for i, t in options[:3]]
    r = requests.post(f"{GRAPH}/{PHONE_NUMBER_ID}/messages",
                      headers={"Authorization": f"Bearer {TOKEN}"},
                      json={"messaging_product": "whatsapp", "to": phone_number,
                            "type": "interactive",
                            "interactive": {"type": "button", "body": {"text": text},
                                            "action": {"buttons": buttons}}},
                      timeout=15)
    if not r.ok:
        print("send failed", r.status_code, r.text)

app = Flask(__name__)

@app.get("/webhook")
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge", ""), 200
    return "wrong verify token", 403

def parse_incoming(body):
    try:
        msg = body["entry"][0]["changes"][0]["value"]["messages"][0]
    except (KeyError, IndexError, TypeError):
        return None                           # delivery receipt etc.
    out = {"id": msg["id"], "from": msg["from"], "kind": None, "text": None, "media_id": None}
    if msg["type"] == "text":
        out["kind"], out["text"] = "text", msg["text"]["body"]
    elif msg["type"] == "image":
        out["kind"], out["media_id"] = "image", msg["image"]["id"]
    elif msg["type"] == "interactive" and msg["interactive"]["type"] == "button_reply":
        out["kind"], out["text"] = "button", msg["interactive"]["button_reply"]["id"]
    else:
        return None
    return out


@app.post("/webhook")
def recieve():
    msg = parse_incoming(request.get_json(silent=True))
    if msg and not already_seen(msg["id"]):
        threading.Thread(target=handle_message, args=(msg,), daemon=True).start()
    return "ok", 200

init_database()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
