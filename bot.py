import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", "10000"))
WEBHOOK_URL = os.environ["WEBHOOK_URL"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 DEPLOY MANAGER\n\n"
        "✅ Bot online!\n\n"
        "☁️ Server: Render\n"
        "📦 Project Manager: siap\n"
        "🐙 GitHub: belum terhubung\n"
        "🧠 AI: belum terhubung"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🚀 Bot starting...")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    main()
