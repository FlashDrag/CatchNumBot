from aiogram import Bot, types
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher
from filters import is_admin

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from config import DB_URL, REDIS_URL
from urllib.parse import urlparse
from data_base.ps_db import BotDB


# создание екзепляра класса БД и инициализация соединения с БД
db = BotDB(DB_URL)

# from data_base.sqlite_db import BotDB
# BotDB = BotDB('ugadaika.db')

'''
# обьявляем объект класса Lang и устанавливаем язык
try:
    lang = Lang(config.lang)
except ValueError:
    print(f"Error no localization found for language code: {config.lang}")
'''

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
url = urlparse(REDIS_URL)
try:
    storage = RedisStorage2(host=url.hostname, port=url.port, password=url.password,
                            ssl=True, ssl_cert_reqs=None)
    # print("Redis as storage")
except Exception:
    storage = MemoryStorage()
#     print("MemoryStorage as storage")
# print(storage)
# https://github.com/Latand/tgbot_template/tree/master/tgbot
dp = Dispatcher(bot, storage=storage)

# биндим фильтры
dp.bind_filter(is_admin.IsAdmin)
