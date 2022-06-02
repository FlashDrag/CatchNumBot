# from aiogram.utils.executor import start_webhook
import config
from loader import dp, db, bot
from handlers.user.user_main import register_handlers_user_main
from handlers.user.user_bug import register_handlers_user_bug
from handlers.admin.admin import register_handlers_admin
from utils.number_process import register_handlers_num_process
from utils.commands import set_commands

import logging
import logging.config

logging.config.fileConfig('logging/logging.config',
                        disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def on_startup(dp):
    # await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)
    # Установка команд бота
    await set_commands(bot)
    logger.debug("Бот успешно запущен")
    await bot.send_message(config.ADMINS_ID['Pasha'], f'Bot successfully started!')

async def on_shutdown(dp):
    # await bot.delete_webhook()
    db.close_connect
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.error("DB and stogare closed")


# Регистрация хэндлеров
register_handlers_user_main(dp)
register_handlers_num_process(dp)
register_handlers_admin(dp)
register_handlers_user_bug(dp)

"""
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


