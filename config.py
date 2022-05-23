from os import getenv

TOKEN = '1493272442:AAFvOOO30FNIMxWNCCFGnwv6vVDGPKI2QmM'

# https://github.com/aahnik/webhook-aiogram-heroku - example; 
# https://habr.com/ru/post/655965/  - tutorial
HEROKU_APP_NAME = getenv('pavlibot')

# webhook settings
WEBHOOK_HOST = 'https://pavlibot.herokuapp.com/'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'