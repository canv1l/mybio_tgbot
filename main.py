from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

DATA_FILE = "visitors.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def escape(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    visitors = load_data()

    if user.id not in [u['id'] for u in visitors]:
        visitors.append({
            'id': user.id,
            'username': user.username or '',
            'first_name': user.first_name
        })
        save_data(visitors)

    position = [u['id'] for u in visitors].index(user.id) + 1

    all_users = [
        f"• @{escape(u['username'])}" if u['username'] else f"• {escape(u['first_name'])}"
        for u in visitors
    ]
    others_text = "\n".join(all_users)

    message = (
        "*✨✨✨*\n"
        f"*🔔 Welcome, {escape(user.first_name)}\\! 🔔*\n"
        "*✨✨✨*\n\n"
        f"*⭐ You are the __{position}ᵗʰ__ person interested in my bio\\! ⭐*\n\n"
        f"*👥 People who clicked:*\n{others_text}"
    )

    await update.message.reply_text(
        message,
        parse_mode="MarkdownV2"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token("7663032209:AAHBVmUEVfVxWL5jCFHKbMlEcKzFSnWiLwc").build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()
