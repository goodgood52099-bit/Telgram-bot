from flask import Flask, request
import requests
import os
import openai

app = Flask(__name__)

# 讀取環境變數
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # ✅ 你的 Telegram ID（只允許這個 ID）
OPENAI_KEY = os.environ.get("OPENAI_KEY")

openai.api_key = OPENAI_KEY
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 傳送訊息給 Telegram
def send_message(text, chat_id=CHAT_ID):
    requests.post(f"{TELEGRAM_API}/sendMessage", data={"chat_id": chat_id, "text": text})

# 呼叫 OpenAI
def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Telegram Webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        text = data["message"].get("text")
        chat_id = str(data["message"]["chat"]["id"])  # 轉成字串以便比較

        # ✅ 只回覆你自己的 CHAT_ID
        if chat_id == str(CHAT_ID):
            if text:
                answer = ask_gpt(text)
                send_message(answer, chat_id)
        else:
            # 非本人可選擇忽略或提示
            send_message("⚠️ 你沒有權限使用這個 Bot。", chat_id)

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))