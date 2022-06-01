from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_bug_inline_markup():
    keyboard = InlineKeyboardMarkup(); #наша клавиатура
    key_yes = InlineKeyboardButton(text='📩Просмотреть', callback_data='watch'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    # key_no = InlineKeyboardButton(text='Закрыть', callback_data='close');
    # keyboard.add(key_no);
    return keyboard