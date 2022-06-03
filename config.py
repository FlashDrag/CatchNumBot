from os import getenv
import logging
import logging.config

logging.config.fileConfig('logging/logging.conf',
                        disable_existing_loggers=False)
logger = logging.getLogger(__name__)


TOKEN = '1493272442:AAFJXt_KdE7pSSoTkgxeu9w5OmtSsmjFEio'
DB_URL = 'postgres://brcogyalzqsmgd:60830c517fe2a7e5dd5a0580ede9248bea915a4a46adc4f058a08a907d149411@ec2-63-34-180-86.eu-west-1.compute.amazonaws.com:5432/dbcfdffpk71b19'
REDIS_URL = 'rediss://:p5a87db47636f08b80eab2da5d1840e5d90c5a2fe188befa41b166f046a51d56c@ec2-3-251-43-118.eu-west-1.compute.amazonaws.com:15710'



# from urllib.parse import urlparse
# url = urlparse(DB_URL)
# print(f'hostname: {url.hostname}\n port: {url.port}\n database: {url.path}\n username: {url.username}\n password: {url.password}')

ADMINS_ID = {'Pasha': 1359618407}
'''
# переменные окружения
TOKEN = getenv('TOKEN')
if not TOKEN:
    logger.critical(f'Failed to get the `TOKEN` variable from env')
    exit(-1)
DB_URL = getenv('DATABASE_URL')
if not DB_URL:
    logger.critical(f'Failed to get the `DATABASE_URL` variable from env')
    exit(-1)
REDIS_URL = getenv('REDIS_TLS_URL')
if not REDIS_URL:
    logger.critical(f'Failed to get the `REDIS_TLS_URL` variable from env')
    exit(-1)

'''
'''

HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')
# TOKEN, HEROKU_APP_NAME – мы считываем из переменных окружения, которые скоро добавим в наш проект.

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
# WEBHOOK_HOST – доменное имя нашего приложения
# https://github.com/Yarolf/async-telegram-bot-with-webhooks-on-heroku/blob/master/heroku-test/config.py 

WEBHOOK_PATH = f'/webhook/{TOKEN}'
# часть пути, на который мы будем принимать запросы. Его следует придумать таким, чтобы не было возможности его угадать,
# во избежание фальсификации запросов. В нашем случае используется токен бота, так как его, также, следует держать в секрете.

WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
# полный url адрес, на который будут принимать запросы.

# webserver settings
WEBAPP_HOST = '0.0.0.0'
# хост нашего приложения, оставляем локальный.

WEBAPP_PORT = getenv('PORT', default=8000)
# порт, на котором работает наше приложение, так же считывается с переменных окружения,
# которое предоставляет Heroku, его мы не заполняем.
'''

# https://github.com/aahnik/webhook-aiogram-heroku - example; 
# https://habr.com/ru/post/655965/  - tutorial

