from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = "8821883241:AAGniYL3Tc3Gdm__9IChOx-UwiL-gaqiK8s"

# Penyimpanan sementara untuk tahap awal
projects = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📁 PROJECTS", callback_data="projects"),
            InlineKeyboardButton("➕ NEW PROJECT", callback_data="new_project"),
        ],
        [
            InlineKeyboardButton("📤 UPLOAD FILE", callback_data="upload"),
            InlineKeyboardButton("📄 GET FILE", callback_data="get_file"),
        ],
        [
            InlineKeyboardButton("🚀 DEPLOY", callback_data="deploy"),
            InlineKeyboardButton("📊 STATUS", callback_data="status"),
        ],
    ]

    await update.message.reply_text(
        "🤖 DEPLOY MANAGER\n\n"
        "Selamat datang!\n\n"
        f"📦 Project: {len(projects)}\n"
        "🌐 Website: 0\n\n"
        "Pilih menu:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "projects":
        if not projects:
            await query.message.reply_text(
                "📁 PROJECTS\n\n"
                "Belum ada project.\n\n"
                "Tekan ➕ NEW PROJECT untuk membuat project."
            )
            return

        text = "📁 PROJECTS\n\n"

        for project_id, name in projects.items():
            text += f"🆔 {project_id} — {name}\n"

        await query.message.reply_text(text)

    elif query.data == "new_project":
        context.user_data["creating_project"] = True

        await query.message.reply_text(
            "➕ NEW PROJECT\n\n"
            "Kirim nama project.\n\n"
            "Contoh:\n"
            "Portofolio"
        )

    elif query.data == "upload":
        await query.message.reply_text(
            "📤 UPLOAD FILE\n\n"
            "Fitur upload akan kita aktifkan setelah sistem project selesai."
        )

    elif query.data == "get_file":
        await query.message.reply_text(
            "📄 GET FILE\n\n"
            "Fitur ini akan mengambil file dari GitHub."
        )

    elif query.data == "deploy":
        await query.message.reply_text(
            "🚀 DEPLOY\n\n"
            "Sistem deploy GitHub Pages akan kita pasang setelah GitHub terhubung."
        )

    elif query.data == "status":
        await query.message.reply_text(
            "📊 STATUS\n\n"
            f"📦 Total project: {len(projects)}\n"
            "🌐 Website online: 0"
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("creating_project"):
        return

    name = update.message.text.strip()

    if not name:
        await update.message.reply_text("❌ Nama project tidak boleh kosong.")
        return

    project_id = len(projects) + 1

    projects[project_id] = name

    context.user_data["creating_project"] = False

    await update.message.reply_text(
        "✅ PROJECT BERHASIL DIBUAT!\n\n"
        f"🆔 ID: {project_id}\n"
        f"📁 Nama: {name}\n\n"
        "Project siap digunakan."
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        # Menangkap teks untuk pembuatan project
        __import__("telegram.ext", fromlist=["MessageHandler"]).MessageHandler(
            __import__("telegram.ext", fromlist=["filters"]).filters.TEXT
            & ~__import__("telegram.ext", fromlist=["filters"]).filters.COMMAND,
            text_handler,
        )
    )

    print("BOT SUDAH ONLINE")

    app.run_polling()


if __name__ == "__main__":
    main()