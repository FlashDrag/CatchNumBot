from os import getenv

TOKEN = getenv('TOKEN')


# https://github.com/Yarolf/async-telegram-bot-with-webhooks-on-heroku/blob/master/heroku-test/config.py 
# переменные окружения
HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = getenv('PORT', default=8000)
DB_URL = getenv('DATABASE_URL')

# https://github.com/aahnik/webhook-aiogram-heroku - example; 
# https://habr.com/ru/post/655965/  - tutorial