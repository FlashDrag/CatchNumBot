from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.number_process import process_start_button
from keyboards.keyboard_markup import *
from keyboards.inline_markup import *
from loader import bot
import logging
# from operator import itemgetter 
from loader import dp

from data_base.ps_db import BotDB


async def process_main_menu(message: types.Message):
    await bot.send_message(message.from_user.id, "Головне меню", reply_markup=main_start_menu_markup())


async def process_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    # if (not BotDB.user_exists(user_id)):
    BotDB.add_user(user_id, first_name, last_name, username)
    rec = BotDB.get_user_name(user_id)
    # print(rec)
    # await state.update_data(user_name=message.from_user.first_name)
    # user_data = await state.get_data()
    '''
    if user_data["user_name"] not in users:
        users[user_data["user_name"]] = 0
        # устанавливаем лвл на ноль если игрока нету в списке
    '''
    await message.answer(f'Привіт {rec} 👋🏻  Це ігра "Вгадайка"')
    await message.answer('Вгайдай-ка число, яке я загадав-ка🤔')
    await message.answer('Додаткова інфа в меню - Допомога або введи /help', reply_markup=main_menu_markup())
    question = f'🏹----------Розпочнемо⁉️----------🎯'
    await message.answer(question, reply_markup=start_inline_markup())
    


async def process_start_command():
    await process_start_button()


@dp.message_handler(commands="cancel", state="*")
async def process_cancel_command(message: types.Message, state: FSMContext):
    # Allow user to cancel any action
    # current_state = await state.get_state()
    # if current_state is None:
    #     await message.reply('current state is None')
    #     return
    # logging.info("Cancelling state %r", current_state)
    await state.reset_state(with_data=False)
    await message.reply('Лади, коли надумаєш зіргати введи СТАРТ', reply_markup=main_start_menu_markup())


async def process_help_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Важко? Я приберіг для тебе 🔽підказку🔽", reply_markup=help_menu_markup())
    await state.reset_state(with_data=False)


async def process_info_command(message: types.Message):
    await message.answer("Це 2-га бета версія ігри з рівнями. З кожним виграшом, рівень підвищується та збільшується діапазон цифр")
    await message.answer('Цю ігру можливо  в̷и̷г̷р̷а̷т̷и̷  ✔️вигравати за мінімальну к-сть спроб.\nКількість спроб є різною для кожного рівня')
    await message.answer('Помітив баги? роби скрін та відправляй в приват(тільки не боту😅) а мені: @pavmys', reply_markup=start_menu_markup())


async def process_reset_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        logging.info("RESETING data %r", data)
        await state.finish()
        await message.reply('Скидання успішне!', reply_markup=start_menu_markup())


async def process_pidkaska_command(message: types.Message, state: FSMContext):
    # await query.answer("Підказка 🧐", show_alert=True)
    await message.reply('З допомою цього алгорифму ти ніколи не програєш 🤯')
    await bot.send_message(message.from_user.id, '👉🏻Це математичний трюк, який називається\nбінарний пошук числа',\
         reply_markup=help_inline_markup())
    await state.reset_state(with_data=False)
    # start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # start_markup.row("Старт")
    # await bot.send_message(message.from_user.id, 'Летсгоушки?', reply_markup=start_markup, reply_markup=help_inline_markup())
        # підказка: кожен раз ділимо на 2 діапазон, що залишився


async def process_progress_command(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        await bot.send_message(message.from_user.id, f"Підкорено рівень №{user_data['win']} в діапазоні {int(user_data['max_num'] / 2)}")
        await bot.send_message(message.from_user.id, f"Настпуний рівень в діапазоні {int(user_data['max_num'])}", reply_markup=start_menu_markup())
    except KeyError:
        await bot.send_message(message.from_user.id, f"Рівень баклажан 🤨", reply_markup=start_menu_markup())
    await state.reset_state(with_data=False)


# async def process_rating(message: types.Message, state: FSMContext):
#     for key, value in sorted(users.items(), key = itemgetter(1), reverse = True):
#         await message.answer(f'{key} - {value}-й рівень')


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(process_main_menu, text="◀️Головне меню", state=None)
    dp.register_message_handler(process_start_button, Text(equals=["🟠Старт", "СТАРТ"], ignore_case=True), state=None)
    dp.register_message_handler(process_welcome, commands="start", state=None)
    dp.register_message_handler(process_cancel_command, commands="cancel", state="*")
    dp.register_message_handler(process_cancel_command, Text(equals=['cancel', 'stop', 'стоп', "❌Відміна"], ignore_case=True), state="*")
    dp.register_message_handler(process_help_command, text="❓Допомога", state="*")
    dp.register_message_handler(process_help_command, commands="help", state="*")
    dp.register_message_handler(process_info_command, commands="info", state="*")
    dp.register_message_handler(process_info_command, text="ℹ️nfo", state="*")
    dp.register_message_handler(process_reset_command, commands=["reset"], state=None)
    dp.register_message_handler(process_reset_command, text="🗑Ресет", state=None)
    dp.register_message_handler(process_pidkaska_command, text="💬Підказка", state="*")
    dp.register_message_handler(process_progress_command, commands=["progress"], state=None)
    dp.register_message_handler(process_progress_command, text="🏅Мій прогрес", state=None)
    # dp.register_message_handler(process_rating, text="🏆Рейтинг", state="*")