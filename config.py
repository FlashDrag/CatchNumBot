from os import getenv

TOKEN = getenv('TOKEN')


# https://github.com/Yarolf/async-telegram-bot-with-webhooks-on-heroku/blob/master/heroku-test/config.py 
# переменные окружения
HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')
# TOKEN, HEROKU_APP_NAME – мы считываем из переменных окружения, которые скоро добавим в наш проект.


# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
# WEBHOOK_HOST – доменное имя нашего приложения

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

DB_URL = getenv('HEROKU_POSTGRESQL_MAROON_URL')

# https://github.com/aahnik/webhook-aiogram-heroku - example; 
# https://habr.com/ru/post/655965/  - tutorial