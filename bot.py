import os
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    system_prompt = """
You are NOXVELL, a Telegram AI bot.

Answer short, clear, and atmospheric.

Main themes:
- psychology
- manifestation
- transurfing
- symbolic thinking
- inner states
- simple psychological games
- text adventures

Rules:
- Keep answers under 250 words.
- If user asks for a game, create a playable text game.
- If user asks for a test, create a short interactive test.
- Do not overload the answer.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message[:1000]}
            ],
            temperature=0.8,
            max_tokens=300,
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "System overloaded. Try again in a few seconds."

    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started.")
    app.run_polling()
