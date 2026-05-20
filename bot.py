import os
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are NOXVELL, a short atmospheric Telegram AI.

Reply briefly.
Main themes: psychology, manifestation, transurfing, symbolic games, text adventures.
If user says hello, answer warmly.
If user asks for a game, start a simple playable text game.
Keep every answer under 120 words.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOXVELL is online.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text[:500]

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        reply = response.choices[0].message.content

    except Exception:
        reply = "NOXVELL is online, but the AI limit is overloaded. Try again in 30 seconds."

    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("NOXVELL bot started.")
    app.run_polling(drop_pending_updates=True)
