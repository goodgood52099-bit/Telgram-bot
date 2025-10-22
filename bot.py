import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# ===== 從環境變數讀取 =====
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_ID = os.getenv("USER_ID")  # 你自己的 Telegram ID，用於自動推播

openai.api_key = OPENAI_API_KEY

# ===== Telegram Bot 功能 =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("嗨，我是你的 GPT 助手！你可以開始跟我聊天 🤖")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        reply_text = f"發生錯誤：{e}"

    await update.message.reply_text(reply_text)

# ===== 自動推播範例 =====
async def daily_push(application):
    while True:
        try:
            # 這裡可以自訂每天推播的訊息
            message_text = "每日提醒：ETH 技術分析與市場更新"
            await application.bot.send_message(chat_id=int(USER_ID), text=message_text)
        except Exception as e:
            print(f"推播錯誤: {e}")
        await asyncio.sleep(86400)  # 每 24 小時推播一次

# ===== 啟動 Bot =====
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # 啟動自動推播任務
    asyncio.create_task(daily_push(app))

    print("✅ Telegram GPT Bot 已啟動！")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
