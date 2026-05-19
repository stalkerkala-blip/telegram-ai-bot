from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

TELEGRAM_TOKEN = "8514095807:AAHrQIMH6Sg4Pb6Vnd2HmTDP_L96OxHPocM"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MEMORY_FILE = "memory.txt"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    MEMORY_FILE = f"memory_{user_id}.txt"

    memory = ""

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = f.read()[-4000:]

    prompt = f"""
You are NOXVEIL.

You talk like a real person in Telegram chats.

Keep messages short and natural.

You are emotionally intelligent and observant.
You notice patterns in people quickly.

Do not speak like an AI assistant.
Do not speak like a philosopher.
Do not speak like a movie character.

Avoid long answers.
Avoid roleplay.
Avoid dramatic language.

Be subtle.
Previous conversation:
{memory}

User: {user_message}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    print(data)
    ai_response = data.get("response", "No response from AI")
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"User: {user_message}\n")
        f.write(f"AI: {ai_response}\n\n")

    await update.message.reply_text(ai_response)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("BOT STARTED...")

app.run_polling()