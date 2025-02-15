import logging
import psutil
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler
from config import TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_server_load():
    """Собирает информацию о загрузке сервера."""
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return (f"💻 *Серверная нагрузка:*\n"
            f"🔹 CPU: {cpu_usage}%\n"
            f"🔹 RAM: {mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)\n"
            f"🔹 Диск: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")

async def start(update: Update, context):
    await update.message.reply_text("Привет! Отправь /status, чтобы узнать загрузку сервера.")

async def status(update: Update, context):
    load_info = await get_server_load()
    await update.message.reply_text(load_info, parse_mode="Markdown")

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    logger.info("Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())  # Используем существующий event loop
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            logger.warning("Event loop уже запущен. Запускаем main() через ensure_future.")
            asyncio.ensure_future(main())  # Запускаем бота в существующем loop
            loop.run_forever()  # Держим процесс активным
        else:
            raise
