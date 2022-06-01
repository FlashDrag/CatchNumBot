from aiogram.utils.executor import start_webhook
import config
from loader import dp, db, bot
from handlers.user.user_main import register_handlers_user_main
from handlers.user.user_bug import register_handlers_user_bug
from handlers.admin.admin import register_handlers_admin
from utils.number_process import register_handlers_num_process
from utils.commands import set_commands
# import logging

from loguru import logger

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(
#     level=logging.INFO,
#     format = "%(asctime)s/%(levelname)s/%(module)s/%(funcName)s: %(lineno)d - %(message)s",
#     )
# logger = logging.getLogger("bot")
# logger.setLevel(logging.DEBUG)

async def on_startup(dp):
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)
    # Установка команд бота
    await set_commands(bot)
    logger.debug("Бот успешно запущен")


async def on_shutdown(dp):
    await bot.delete_webhook()
    db.close_connect
    logger.error("БД отключена")
    await dp.storage.close()
    await dp.storage.wait_closed()

# Регистрация хэндлеров
register_handlers_user_main(dp)
register_handlers_num_process(dp)
register_handlers_admin(dp)
register_handlers_user_bug(dp)


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

"""
from aiogram.utils import executor
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True, on_shutdown=on_shutdown)
"""

