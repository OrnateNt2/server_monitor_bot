import logging
import psutil
import telegram
from telegram.ext import Updater, CommandHandler
from config import TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_server_load():
    """Собирает информацию о загрузке сервера."""
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return (f"💻 *Серверная нагрузка:*\n"
            f"🔹 CPU: {cpu_usage}%\n"
            f"🔹 RAM: {mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)\n"
            f"🔹 Диск: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")

def start(update, context):
    update.message.reply_text("Привет! Отправь /status, чтобы узнать загрузку сервера.")

def status(update, context):
    load_info = get_server_load()
    update.message.reply_text(load_info, parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
