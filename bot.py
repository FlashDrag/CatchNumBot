from aiogram.utils.executor import start_webhook
import logging
# from data_base.sqlite_db import BotDB
from loader import dp, bot
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers.common import register_handlers_common
from utils.number_process import register_handlers_num_process
import config
from data_base.ps_db import BotDB
dic = {1:"🥇", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "останньої😓"}
users = {}

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def on_startup(dp):
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)
    print("Бот успешно запущен")


async def on_shutdown(dp):
    await bot.delete_webhook()
    BotDB.conn.close()
    BotDB.cursor.close()

# BotDB('ugadaika.db').setup()
register_handlers_common(dp)
register_handlers_num_process(dp)


if __name__ == '__main__':
    start_webhook(
        dispatcher = dp, 
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        webhook_path=config.WEBHOOK_PATH,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )

# BotFather
# start - Запуск Ігри 👊
# progress - Мій рівень 💪
# help - Допомога 🙏
# cancel - Відміна 🖕