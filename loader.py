from aiogram import Bot, types
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from config import DB_URL, REDIS_URL
from urllib.parse import urlparse
from data_base.ps_db import BotDB


# инициализация соединения с БД
db = BotDB(DB_URL)

# from data_base.sqlite_db import BotDB
# BotDB = BotDB('ugadaika.db')


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
url = urlparse(REDIS_URL)
try:
    storage = RedisStorage2(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)
    # print("Redis as storage")
except:
    storage = MemoryStorage()
#     print("MemoryStorage as storage")
# print(storage)
# https://github.com/Latand/tgbot_template/tree/master/tgbot
dp = Dispatcher(bot, storage=storage)

