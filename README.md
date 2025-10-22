# Telegram 智慧生活助手

## 部署步驟

1. 在 Telegram @BotFather 建立 Bot，取得 BOT_TOKEN
2. 跟 Bot 說話取得 chat_id
3. 申請 OpenAI API Key
4. 設定 Render Web Service
   - Build Command: pip install -r requirements.txt
   - Start Command: python app.py
   - Environment Variables:
       BOT_TOKEN=你的BOT_TOKEN
       CHAT_ID=你的chat_id
       OPENAI_KEY=你的OpenAI_KEY
5. 設定 Webhook:
   https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<你的Render網址>/<BOT_TOKEN>
6. 部署完成後，Bot 就能跟你聊天並每天發送提醒
