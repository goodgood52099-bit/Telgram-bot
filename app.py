from flask import Flask, request
import requests
import os
import openai
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OPENAI_KEY = os.environ.get("OPENAI_KEY")

openai.api_key = OPENAI_KEY
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(text):
    requests.post(f"{TELEGRAM_API}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": text
    })

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        text = data["message"].get("text")
        chat_id = data["message"]["chat"]["id"]
        if text:
            answer = ask_gpt(text)
            requests.post(f"{TELEGRAM_API}/sendMessage", data={
                "chat_id": chat_id,
                "text": answer
            })
    return {"ok": True}

def daily_reminder():
    send_message("早安！今天要記得運動、喝水 💧")

scheduler = BackgroundScheduler()
scheduler.add_job(daily_reminder, 'cron', hour=8, minute=0)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
