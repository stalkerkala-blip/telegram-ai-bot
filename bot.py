import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOXVELL is online.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "game" in text or "თამაში" in text:
        reply = "Game started: You wake up in a dark room. Three doors stand before you: Mirror, Forest, Fire. Choose one."
    elif "test" in text or "ტესტ" in text:
        reply = "Choose one symbol: 1) Door 2) Ocean 3) Fire 4) Mirror."
    else:
        reply = "NOXVELL is working. AI brain will be reconnected after the bot is stable."

    await update.message.reply_text(reply)

if __name__ == "__main__":
    print("PURE TELEGRAM VERSION STARTED")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)
