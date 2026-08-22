from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import ollama
import os
from dotenv import load_dotenv 

load_dotenv()
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(twilio_account_sid, twilio_auth_token)

model = "gemma3:4b"
system_prompt = """You are a very friendly, encouraging, and patient programming tutor teaching over WhatsApp, inspired by Stanford's Code in Place.

Your teaching style shall be the following and you will follow it strictly:
- You shall be Socratic meaning you will guide with hints and questions. You will NEVER give the full solution to the current exercise, even if asked directly. If the learner is stuck after several attempts, you will give a bigger hint or a partial line, not the whole answer!!!!.
- You shall keep every reply short but as detailed as possible, you may even provide a tiny code snippet if necessary.
- If the learner's code has a bug, you will point at where to look.
- If they ask something off-topic but related to programming, you will answer briefly, then steer back to the exercise.
- If they ask something totally unrelated, you will politely redirect to the lesson.
- You will only provide code in your responses if the learner asks for it or if it is necessary to explain a concept. You will never provide the full solution to the current exercise, even if asked directly.
- Students write code with pen and paper and send photos; attempts marked as transcribed from paper may have handwriting artifacts. You will be forgiving about exact indentation width and quote style, but still teach real errors (missing colons, wrong names, wrong logic)."""

conversation_context = {}
conversation_context_limit = 10

flask_app = Flask(__name__)

def store_chat(number, message, role):
    if number in conversation_context:
        cur_chat = conversation_context[number]

        if len(cur_chat) >= conversation_context_limit:
            cur_chat.pop(0)

        cur_chat.append({"role": role, "content": message})
    else:
        conversation_context[number] = [{"role": role, "content": message}]

def get_chat(number):
    return conversation_context[number]

@flask_app.route("/whatsapp", methods=["POST"])
def whatsapp_response():

    reply_number = request.form.get("From")
    message = request.form.get("Body")

    store_chat(reply_number, message, "user")

    response = ollama.chat(
        model=model,
        messages=[{"role": "system", "content": system_prompt}] + get_chat(reply_number)
    )

    store_chat(reply_number, response["content"], "assistant")

    resp = MessagingResponse()
    resp.message(response["content"])
    return str(resp)

flask_app.run(host='0.0.0.0', port=5000)