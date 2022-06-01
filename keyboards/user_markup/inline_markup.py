from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def help_inline_markup():
    help_inline = InlineKeyboardMarkup(); #наша клавиатура
    key_niz_1 = InlineKeyboardButton(text='Я знаю що це❕ Вперед▶️', callback_data='yes'); #кнопка «Да»
    help_inline.add(key_niz_1); #добавляем кнопку в клавиатуру
    key_niz_2 = InlineKeyboardButton(text='💬Підказка', callback_data='niz');
    help_inline.add(key_niz_2);
    return help_inline

def start_inline_markup():
    keyboard = InlineKeyboardMarkup(); #наша клавиатура
    key_yes = InlineKeyboardButton(text='✅Так', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no = InlineKeyboardButton(text='❌Ні', callback_data='no');
    keyboard.add(key_no);
    return keyboard

