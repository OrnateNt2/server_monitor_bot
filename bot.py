import os
import psutil
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "0"))

# Настраиваем логирование
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def check_auth(update: Update) -> bool:
    """Проверяем, что запрос от разрешенного пользователя."""
    user_id = update.effective_user.id
    if user_id != ALLOWED_USER_ID:
        update.message.reply_text("⛔ Доступ запрещён!")
        return False
    return True

def get_server_status() -> str:
    """Получаем информацию о сервере."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    status = (f"💻 *Состояние сервера:*
"
              f"🖥 *CPU:* {cpu_usage}%
"
              f"🗄 *RAM:* {memory.percent}% (использовано {memory.used // (1024**3)} ГБ из {memory.total // (1024**3)} ГБ)
"
              f"💾 *Диск:* {disk.percent}% (использовано {disk.used // (1024**3)} ГБ из {disk.total // (1024**3)} ГБ)")
    return status

async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    if not check_auth(update):
        return
    await update.message.reply_text("Привет! Я бот для мониторинга состояния сервера. Используй /status для проверки.")

async def status(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /status"""
    if not check_auth(update):
        return
    status_text = get_server_status()
    await update.message.reply_text(status_text, parse_mode='Markdown')

# Настраиваем бота
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("status", status))

if __name__ == "__main__":
    logger.info("Бот запущен...")
    app.run_polling()
