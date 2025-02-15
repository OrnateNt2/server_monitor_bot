import os
import psutil
import logging
import subprocess
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

def get_memory_info():
    """Получает корректную информацию о памяти в контейнере"""
    try:
        result = subprocess.run(["free", "-b"], capture_output=True, text=True).stdout
        lines = result.split("\n")
        mem_line = lines[1].split()
        total_memory = int(mem_line[1])
        used_memory = int(mem_line[2])
        return total_memory, used_memory
    except Exception as e:
        return 0, 0

def get_additional_info() -> str:
    """Получаем дополнительную информацию с помощью shell-скрипта."""
    try:
        result = subprocess.run(["sh", "server_info.sh"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Ошибка при получении данных: {str(e)}"

def get_server_status() -> str:
    """Получаем информацию о сервере."""
    cpu_usage = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage('/')

    total_memory, used_memory = get_memory_info()

    additional_info = get_additional_info()

    status = (f"💻 *Состояние сервера:*\n"
              f"🖥 *CPU:* {cpu_usage}%\n"
              f"🗄 *RAM:* {(used_memory / total_memory * 100) if total_memory else 0:.1f}% "
              f"(использовано {used_memory // (1024**3)} ГБ из {total_memory // (1024**3)} ГБ)\n"
              f"💾 *Диск:* {disk.percent}% (использовано {disk.used // (1024**3)} ГБ из {disk.total // (1024**3)} ГБ)\n"
              f"🔍 *Доп. информация:*\n{additional_info}")
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
