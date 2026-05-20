import os
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are NOXVELL, a short atmospheric Telegram AI.
Answer under 100 words.
Themes: psychology, manifestation, transurfing, symbolic games, text adventures.
"""

def offline_reply(text):
    t = text.lower()

    if "hello" in t or "hey" in t or "hi" in t or "გამარჯობა" in t:
        return "NOXVELL is online. I hear you."

    if "game" in t or "adventure" in t or "თამაში" in t:
        return "Game started: You wake up in a dark room. There are three doors: Mirror, Forest, and Fire. Choose one."

    if "test" in t or "ტესტ" in t:
        return "Quick test: choose one symbol — 1) Door 2) Ocean 3) Fire 4) Mirror. I will interpret your choice."

    return "NOXVELL is online. AI limit is overloaded right now, but the bot is working."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOXVELL is online.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text[:400]

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        reply = response.choices[0].message.content
    except Exception:
        reply = offline_reply(user_message)

    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("NOXVELL bot started.")
    app.run_polling(drop_pending_updates=True)
