from flask import Flask, request
import requests
import os
import openai
import traceback

app = Flask(__name__)

# 環境變數
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # 只回覆自己
OPENAI_KEY = os.environ.get("OPENAI_KEY")
openai.api_key = OPENAI_KEY

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 傳訊息到 Telegram
def send_message(text, chat_id=CHAT_ID):
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print("❌ Telegram 傳訊息錯誤：", e)

# 呼叫 GPT
def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("⚠️ GPT 呼叫錯誤：", e)
        traceback.print_exc()
        return f"AI 回覆發生錯誤：{e}"

# Telegram Webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("📩 收到 Telegram JSON：", data)

        if not data or "message" not in data:
            return {"ok": False}

        message = data["message"]
        chat_id = str(message["chat"]["id"])

        # 只回覆自己
        if chat_id != str(CHAT_ID):
            send_message("⚠️ 你沒有權限使用這個 Bot。", chat_id)
            return {"ok": True}

        # 處理文字訊息
        if "text" in message and message["text"]:
            text = message["text"]
            answer = ask_gpt(text)
            send_message(answer, chat_id)
            return {"ok": True}

        # 處理圖片訊息
        elif "photo" in message and message["photo"]:
            photo_file_id = message["photo"][-1]["file_id"]
            send_message(f"✅ 收到你的圖片！File ID: {photo_file_id}", chat_id)
            return {"ok": True}

        # 處理影片訊息
        elif "video" in message and message["video"]:
            video_file_id = message["video"]["file_id"]
            send_message(f"✅ 收到你的影片！File ID: {video_file_id}", chat_id)
            return {"ok": True}

        # 處理其他訊息
        else:
            send_message("⚠️ 目前只支援文字、圖片和影片。", chat_id)
            return {"ok": True}

    except Exception as e:
        print("🔥 webhook 發生錯誤：", e)
        traceback.print_exc()
        return {"ok": False}

if __name__ == "__main__":
    print("🚀 Flask 伺服器啟動中...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
