import os
from groq import Groq
from tavily import TavilyClient
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

MEMORY_FILE = "memory.txt"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()[-1500:]
    return ""


def save_memory(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(text[:500] + "\n")


def search_internet(query):
    try:
        result = tavily.search(
            query=query,
            search_depth="basic",
            max_results=1
        )

        info = ""
        for r in result.get("results", []):
            content = r.get("content", "")
            info += content[:700] + "\n"

        return info[:1000]

    except Exception:
        return ""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    memory = load_memory()
    internet_info = search_internet(user_message)

    system_prompt = f"""
You are NOXVELL, an atmospheric psychological AI inside Telegram.

Your main themes:
- Transurfing
- Manifestation
- Psychology
- Symbolism
- Inner states
- Atmospheric dialogue
- Simple psychological games
- Text-based interactive adventures

Rules:
- Answer clearly.
- Do not write too long.
- If the user asks for a game, create a playable text game.
- If the user asks for a test, create a short interactive test.
- Use internet info only when useful.
- Keep answers atmospheric but practical.

Memory:
{memory}

Internet info:
{internet_info}
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=500,
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "System overloaded. Try again with a shorter message."

    save_memory(f"USER: {user_message}")
    save_memory(f"AI: {reply}")

    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
