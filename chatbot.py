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
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
MAX_VIDEO_BYTES = 16 * 1024 * 1024 

def init_database():
    with database() as c:
        c.executescript("""CREATE TABLE IF NOT EXISTS students (
                                phone TEXT PRIMARY KEY,
                                current_lesson INTEGER NOT NULL DEFAULT 1,
                                current_step INTEGER NOT NULL DEFAULT 0,
                                attempts INTEGER NOT NULL DEFAULT 0,
                                score INTEGER NOT NULL DEFAULT 0);
                            CREATE TABLE IF NOT EXISTS events (phone TEXT, event TEXT, detail TEXT, ts REAL);
                            CREATE TABLE IF NOT EXISTS seen_messages (id TEXT PRIMARY KEY, ts REAL);
                            CREATE TABLE IF NOT EXISTS uploads (path TEXT PRIMARY KEY, mtime REAL, media_id TEXT, ts REAL);
                            CREATE TABLE IF NOT EXISTS chats (phone TEXT, role TEXT, content TEXT, ts REAL);""")

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

OLLAMA_CHAT_MODEL = "llama3.2"
ASK_HISTORY = 6

TUTOR_PROMPT = """You are a friendly, patient Python tutor on WhatsApp for beginners following Harvard's CS50P course.
Students write code with pen and paper, then photograph it or type it.

Rules you must follow:
- Be Socratic: guide with hints and questions. NEVER give the answer to the student's current question or the full solution to their current task, even if they ask directly.
- Keep replies short: under 800 characters.
- Plain text only. No markdown: no ** or # headings - WhatsApp shows them as symbols.
- You may show a tiny code example of 1-3 lines, but use a different example from the current task.
- If the question is not about programming, politely steer back to the lesson.

Where the student is right now:
Lesson: {lesson}
Current step: {step}"""

def ask_tutor(phone, student, question):
    lesson = LESSONS[student["current_lesson"]]["title"]
    step = current_step(student)
    context = step["text"] if step else "between lessons"
    with database() as c:
        rows = c.execute("SELECT role, content FROM chats WHERE phone = ? ORDER BY ts DESC LIMIT ?",
                         (phone, ASK_HISTORY)).fetchall()
    history = [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]
    response = ollama.chat(
        model=OLLAMA_CHAT_MODEL,
        messages=[{"role": "system", "content": TUTOR_PROMPT.format(lesson=lesson, step=context)}]
                 + history + [{"role": "user", "content": question}],
        options={"num_predict": 300})
    reply = response["message"]["content"].strip().replace("**", "*")
    now = time.time()
    with database() as c:
        c.execute("INSERT INTO chats VALUES (?, 'user', ?, ?)", (phone, question, now))
        c.execute("INSERT INTO chats VALUES (?, 'assistant', ?, ?)", (phone, reply, now + 0.001))
    return reply


WELCOME = ("Welcome to Pypaper! Learn Python with just a pen and paper. \n"
           "The lessons follow Harvard's free CS50P course.\n\n"
           "Never write your name on pages you photograph.\n\n"
           "Stuck? Start a message with ASK to ask me anything.\n"
           "Type HELP anytime you feel lost or want commands. Type START to begin!")

HELP = ("Commands:\n"
        "START - begin or continue\n"
        "PROGRESS - see your score\n"
        "RESTART - start the current lesson again\n"
        "HELP - this message\n\n"
        "RESET - wipe your progress and start from Lesson 1\n"
        "ASK ... - ask me a question, e.g.  ASK what does return do?\n"
        "VIDEO - videos that explain this lesson\n"
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

    ask = re.match(r"\s*ask\b[\s:,.-]*(.*)", message["text"] or "", re.IGNORECASE | re.DOTALL)
    if ask and message["kind"] == "text":
        handle_ask(phone, student, ask.group(1).strip())
        return
    
    cmd = normalise(message["text"] or "").upper()
    step = current_step(student)
    if cmd == "HELP":
        send_message(phone, HELP)
    elif cmd == "VIDEO":
        send_lesson_videos(phone, student)
    elif cmd == "PROGRESS":
        send_message(phone, f"📊 Lesson {student['current_lesson']}, "
                            f"step {student['current_step'] + 1}. Score: {student['score']} ⭐")
    elif cmd == "RESTART":
        update_student(phone, current_step=0, attempts=0)
        present(phone, get_student(phone))
    elif cmd == "RESET":
        with database() as c:
            c.execute("DELETE FROM students WHERE phone = ?", (phone,))
        send_message(phone, "Progress wiped. Type START to begin again from Lesson 1.")
    elif cmd == "START" or step is None or step["type"] in ("teach", "video"):
        present(phone, student)               
    else:
        check_answer(phone, student, step, message["text"])

def handle_ask(phone, student, question):
    if not question:
        send_message(phone, "Type your question after ASK, e.g.\nASK what does return do?")
        return
    send_message(phone, "Good question - let me think...")
    try:
        reply = ask_tutor(phone, student, question)
    except Exception as e:
        log_event(phone, "ask_error", str(e)[:200])
        send_message(phone, "Sorry, I can't answer questions right now. Try again in a minute, or type VIDEO.")
        return
    log_event(phone, "ask", question[:200])
    send_message(phone, reply[:1500] + "\n\n(Now carry on with the question above)")


def send_lesson_videos(phone, student):
    lesson = LESSONS[student["current_lesson"]]
    send_message(phone, f"Videos for Lesson {student['current_lesson']}: {lesson['title']}")
    for key in lesson.get("videos", []):
        send_video(phone, key)

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
            send_video(phone, step["video"], intro=step["text"])
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
    else:
        send_message(phone, f"You finished every lesson! Final score: {student['score']}\n\n"
                            "Type RESTART to practise again.")

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

def upload_media(path):
    mtime = os.path.getmtime(path)
    with database() as c:
        row = c.execute("SELECT * FROM uploads WHERE path = ?", (path,)).fetchone()
    if row and row["mtime"] == mtime and time.time() - row["ts"] < 25* 24 * 3600:
        return row["media_id"]
    with open(path, "rb") as f:
        r = requests.post(f"{GRAPH}/{PHONE_NUMBER_ID}/media",
                          headers={"Authorization": f"Bearer {TOKEN}"},
                          files={"file": (os.path.basename(path), f, "video/mp4")},
                          data={"messaging_product": "whatsapp", "type": "video/mp4"},
                          timeout=120)
    if not r.ok:
        print("upload failed", r.status_code, r.text)
        return None
    media_id = r.json()["id"]
    with database() as c:
        c.execute("INSERT OR REPLACE INTO uploads VALUES (?, ?, ?, ?)", (path, mtime, media_id, time.time()))
    return media_id

def send_video(phone_number, key, intro=None):
    video = VIDEOS[key]
    caption = video["title"] + ("\n" + video["credit"] if video.get("credit") else "")
    if intro:
        caption = intro + "\n\n" + caption
    path = os.path.join(BASE_DIR, video["file"]) if video.get("file") else None
    if path and os.path.isfile(path) and os.path.getsize(path) <= MAX_VIDEO_BYTES:
        media_id = upload_media(path)
        if media_id:
            r = requests.post(f"{GRAPH}/{PHONE_NUMBER_ID}/messages",
                              headers={"Authorization": f"Bearer {TOKEN}"},
                              json={"messaging_product": "whatsapp", "to": phone_number,
                                    "type": "video", "video": {"id": media_id, "caption": caption}},
                              timeout=15)
            if r.ok:
                return
            print("video send failed", r.status_code, r.text)
    send_message(phone_number, f"{caption}\n{video['url']}")

def check_answer(phone, student, step, text):
    answer = normalise(text)
    feedback = None

    if step["type"] == "paper": 
        correct = True               
        for pattern, hint in zip(step["patterns"], step["pattern_hints"]):
            if not re.search(pattern, text, re.IGNORECASE):
                correct, feedback = False, f"Not quite. {hint}"
                break
    elif step["type"] == "choice":
        correct = answer == step["answer"].lower()
        feedback = step["wrong"].get(answer)
    else:                                     
        correct = answer in [normalise(a) for a in step["answers"]]
        feedback = step["wrong"].get(answer)

    record_result(phone, student, step, correct, feedback)

def record_result(phone, student, step, correct, feedback):
    attempts = student["attempts"] + 1
    log_event(phone, "answer", f"L{student['current_lesson']}S{student['current_step']}:{'ok' if correct else 'wrong'}")

    if correct:
        if attempts == 1:
            update_student(phone, score=student["score"] + 1)
            send_message(phone, "Correct, first try! +1")
        else:
            send_message(phone, " That's it!")
        present(phone, advance(phone, student))
    elif attempts >= MAXIMUM_ATTEMPTS:        
        if "answers" in step:
            reveal = step["answers"][0]
        elif "options" in step:
            reveal = dict(step["options"]).get(step["answer"], step["answer"])
        else:
            reveal = "\n" + "\n".join(step["pattern_hints"])
        send_message(phone, f"Let's move on. The answer was: {reveal}")
        present(phone, advance(phone, student))
    else:
        update_student(phone, attempts=attempts)
        if feedback:                          
            send_message(phone, feedback + "\n\nTry again!")
        elif attempts == 1:
            send_message(phone, "Hmm, not that. Have another go!")
        else:
            send_message(phone, f"Hint: {step.get('hint', 'Look at the step above once more.')}")


def handle_image(phone, student, media_id):
    step = current_step(student)
    if step is None or step["type"] != "paper":
        send_message(phone, "Nice photo! But this step wants a typed answer. Look at the question above.")
        return
    send_message(phone, "Got it, reading your handwriting... this can take a couple of minutes.")
    try:
        image, mime = download_media(media_id)
        code = transcribe_photo(image)
    except Exception as e:
        log_event(phone, "grade_error", str(e)[:200])
        send_message(phone, "Sorry, I couldn't read that photo right now. Try again in a minute, or type your code instead.")
        return
    send_message(phone, f"I read:\n\n{code}\n\n(If I misread your writing, just type your code instead.)")
    check_answer(phone, student, step, code)

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
        return None                           
    out = {"id": msg["id"], "from": msg["from"], "kind": None, "text": None, "media_id": None}
    if time.time() - int(msg.get("timestamp", time.time())) > 15 * 60:
        return None
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
