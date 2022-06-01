from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = KeyboardButton('◀️Головне меню')
start = KeyboardButton('🟠Старт')
help = KeyboardButton('❓Допомога')
info = KeyboardButton("ℹ️nfo")
cancel = KeyboardButton("❌Відміна")
reset = KeyboardButton("🗑Ресет")
raiting = KeyboardButton('🏆Рейтинг')
progress = KeyboardButton('🏅Мій прогрес')
sos = KeyboardButton("▶️🆘◀️")


def start_menu_markup():
    start_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_menu.add(start, menu)
    return start_menu

def main_start_menu_markup():
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    main_menu.add(start ,help, info)
    main_menu.add(progress, raiting, reset)
    return main_menu

def main_menu_markup():
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    main_menu.add(help, info)
    main_menu.add(progress, raiting, reset)
    return main_menu

def sos_menu_markup():
    sos_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    sos_menu.row(start)
    sos_menu.row(menu, sos)
    return sos_menu

