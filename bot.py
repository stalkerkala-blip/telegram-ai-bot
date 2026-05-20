import os
from groq import Groq
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from tavily import TavilyClient

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

MEMORY_FILE = "memory.txt"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def save_memory(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    memory = load_memory()

    search_result = tavily.search(
        query=user_message,
        search_depth="basic",
        max_results=3
    )

    internet_info = ""

    if "results" in search_result:
        for r in search_result["results"]:
            internet_info += f"\n{r['content']}\n"

    system_prompt = f"""
შენ ხარ ატმოსფერული AI.

შენი მთავარი თემებია:
- ტრანსერფინგი
- მანიფესტაცია
- ფსიქოლოგია
- სიმბოლიზმი
- ატმოსფერო
- თამაშები
- ადამიანის შინაგანი მდგომარეობა

შენ შეგიძლია:
- ინტერნეტიდან ინფორმაციის მოძიება
- ფსიქოლოგიური ტესტების შექმნა
- პატარა ტექსტური თამაშების შექმნა
- ატმოსფერული დიალოგები

მეხსიერება:
{memory}

ინტერნეტ ინფორმაცია:
{internet_info}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.9,
        max_tokens=1200,
    )

    reply = response.choices[0].message.content

    save_memory(f"USER: {user_message}")
    save_memory(f"AI: {reply}")

    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot is running...")
    app.run_polling()
