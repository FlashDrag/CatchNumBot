from aiogram.utils.executor import start_webhook
from os import getenv
import logging
# from data_base.sqlite_db import BotDB
from loader import dp, bot
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers.common import register_handlers_common
from utils.number_process import register_handlers_num_process
import config
dic = {1:"🥇", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "останньої😓"}
users = {}

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# https://github.com/aahnik/webhook-aiogram-heroku - example; 
# https://habr.com/ru/post/655965/  - tutorial
HEROKU_APP_NAME = config.HEROKU_APP_NAME

# webhook settings
WEBHOOK_HOST = config.WEBHOOK_HOST
WEBHOOK_PATH = config.WEBHOOK_PATH
WEBHOOK_URL = config.WEBHOOK_URL

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = getenv('PORT', default=8000)



async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print("Бот успешно запущен")


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


# BotDB('ugadaika.db').setup()
register_handlers_common(dp)
register_handlers_num_process(dp)


if __name__ == '__main__':
    start_webhook(
        dp, 
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        webhook_path=WEBHOOK_PATH,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

# BotFather
# start - Запуск Ігри 👊
# progress - Мій рівень 💪
# help - Допомога 🙏
# cancel - Відміна 🖕