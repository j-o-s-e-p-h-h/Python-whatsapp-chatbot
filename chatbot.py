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

model = ollama.Ollama(model="llama2", api_key=os.getenv("OLLAMA_API_KEY"))
system_prompt = 