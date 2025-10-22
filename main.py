# main.py
# ===============================
# 中文版 Telegram + ChatGPT Bot
# ===============================
import os
import requests
import openai
from flask import Flask, request

app = Flask(__name__)

# -------------------------------
# 讀取密鑰（從 Render 環境變數取得）
# -------------------------------
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # Telegram Bot Token
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Telegram API 送訊息網址
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# -------------------------------
# 接收 Telegram 訊息
# -------------------------------
@app.route("/" + BOT_TOKEN, methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"]["text"]

    # 呼叫 ChatGPT 回覆訊息
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 可改成 gpt-4 或 gpt-5
        messages=[{"role": "user", "content": user_message}]
    )
    reply_text = response.choices[0].message["content"]

    # 回覆訊息給 Telegram 使用者
    requests.post(TELEGRAM_URL, data={"chat_id": chat_id, "text": reply_text})
    return "ok", 200

# -------------------------------
# 測試用首頁
# -------------------------------
@app.route("/")
def home():
    return "🤖 Telegram ChatGPT Bot 已啟動！"

# -------------------------------
# Render 啟動入口
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))