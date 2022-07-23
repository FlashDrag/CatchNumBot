from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.number_process import process_start_button
from keyboards.user_markup.keyboard_markup import *
from keyboards.user_markup.inline_markup import *
from loader import bot, db
from aiogram.dispatcher.filters.builtin import Command

import logging
import logging.config

logging.config.fileConfig('logging/logging.conf',
                          disable_existing_loggers=False)
log = logging.getLogger(__name__)


async def process_main_menu(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id, "Головне меню", reply_markup=main_start_menu_markup())


@db.usage_counter
async def process_welcome(message: types.Message, command: Command.CommandObj, state: FSMContext):
    # print(f"{command.args=}")
    # В command.args будет то, что после команды /start
    await state.reset_state(with_data=False)
    async with state.proxy() as data:
        data["name"] = message.from_user.first_name
        data["username"] = message.from_user.username
        # Запоминаем first_name и username юзера в FSM
    db.add_user(message)
    user_id = message.from_user.id
    log.info(f'User {data["name"]} starting game!')
    # db.update_welcome_count(user_id)  #счетчик
    # Добавляем юзера в основную базу
    if data["name"]:
        name = data["name"]
    elif data["username"]:
        name = data["username"]
    else:
        name = "друже"
    # Приветствуем по имени, если нет - то по username
    await message.answer(f'Привіт {name} 👋🏻  Це ігра "Вгадайка🤔"\n '
                         '⁉️Допомога в меню або команда ➡️ /help', reply_markup=main_menu_markup())
    question = f'🏹----------Розпочнемо❓----------🎯'
    await message.answer(question, reply_markup=start_inline_markup())


async def process_start_command(state: FSMContext):
    await state.reset_state(with_data=False)
    await process_start_button()


@db.usage_counter
async def process_cancel_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # db.update_cancel_count(user_id)  # счетчик
    # Allow user to cancel any action
    # current_state = await state.get_state()
    # if current_state is None:
    #     await message.reply('current state is None')
    #     return
    # logging.info("Cancelling state %r", current_state)
    await state.reset_state(with_data=False)
    text = f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n "\
        f"<b>Лади, надумаєш зіграти просто введи слово СТАРТ ⬇️⏺</b> "
    await message.reply(text, reply_markup=main_start_menu_markup())


@db.usage_counter
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # db.update_help_count(user_id)  #счетчик
    await bot.send_message(message.from_user.id, f"З допомою цього алгорифму ти ніколи не програєш 🤯\n "
                                                 "👉🏻Це математичний трюк, який називається\nбінарний пошук числа\n "
                                                 "Досі важко❓❓\n",
                                                 reply_markup=help_inline_markup())
    await state.reset_state(with_data=False)


@db.usage_counter
async def process_info_command(message: types.Message):
    user_id = message.from_user.id
    # db.update_info_count(user_id)  #счетчик
    await message.answer(f"<pre> "
                         "🔸Це 2-га бета версія ігри з рівнями.\n "
                         "🔸З кожним виграшом, рівень підвищується та збільшується діапазон цифр\n "
                         "🔸Цю гру можливо  в̷и̷г̷р̷а̷т̷и̷  ✔️вигравати за мінімальну к-сть спроб.\n "
                         "🔸Кількість спроб є різною для кожного рівня\n "
                         "</pre>"
                         "🟢Помітили баги? Є пропозиції? команда➡️ /bug ", reply_markup=start_menu_markup())


@db.usage_counter
async def process_reset_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # db.update_reset_count(user_id)  # счетчик
    async with state.proxy() as data:
        log.debug(f"RESETING data: {data}")
    await state.finish()
    db.reset_values(user_id)
    await message.reply('Скидання успішне!', reply_markup=start_menu_markup())


@db.usage_counter
async def process_progress_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # db.update_progress_count(user_id)  # счетчик
    win_count = db.get_win_count(user_id)
    max_num = db.get_max_num(user_id)
    if win_count + 1 == 1:
        await bot.send_message(message.from_user.id, f"Рівень баклажан 🤨", reply_markup=start_menu_markup())
    else:
        await bot.send_message(message.from_user.id, f"🧮Підкорено діапазон {int(max_num / 2)}🔻")
        await bot.send_message(message.from_user.id, f"📈Наступний рівень №{win_count + 1} в діапазоні {max_num}🔺",
                                                     reply_markup=start_menu_markup())
    await state.reset_state(with_data=False)


@db.usage_counter
async def process_rating(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # db.update_rating_count(user_id)  # счетчик
# async with state.proxy() as data:
#     data[“111”] = message.text
    await bot.send_message(message.from_user.id, f'<pre>{db.get_rating(message)}</pre>',
                                                 reply_markup=start_menu_markup())
    await state.reset_state(with_data=False)


async def process_sos(message: types.Message):
    from config import ADMINS_ID as ad_id
    # async with state.proxy() as data:
    #     name = data["name"]
    user_id = message.from_user.id
    if message.chat.first_name:
        name = message.chat.first_name
    else:
        name = message.chat.username
    # ссылка на юзера tg://user?id={user_id}
    await bot.send_message(ad_id[0], f'SOS от: <a href="tg://user?id={user_id}">{name}</a>')
    await message.reply(f'Админ свяжеться с тобой как только сможет. Спасибо!', reply_markup=start_menu_markup())


def register_handlers_user_main(dp: Dispatcher):
    dp.register_message_handler(process_main_menu, text="◀️Головне меню", state="*")
    dp.register_message_handler(process_start_button, Text(equals=["🟠Старт", "СТАРТ"], ignore_case=True), state="*")
    dp.register_message_handler(process_welcome, Command(commands=["start"]), state='*')
    dp.register_message_handler(process_cancel_command, commands="cancel", state="*")
    dp.register_message_handler(process_cancel_command, Text(equals=['cancel', 'stop', 'стоп', "❌Відміна"],
                                                             ignore_case=True), state="*")
    dp.register_message_handler(process_help_command, text="❓Допомога", state="*")
    dp.register_message_handler(process_help_command, commands="help", state="*")
    dp.register_message_handler(process_info_command, commands="info", state="*")
    dp.register_message_handler(process_info_command, text="ℹ️nfo", state="*")
    dp.register_message_handler(process_reset_command, commands=["reset"], state=None)
    dp.register_message_handler(process_reset_command, text="🗑Ресет", state=None)
    dp.register_message_handler(process_progress_command, commands=["progress"], state=None)
    dp.register_message_handler(process_progress_command, text="🏅Мій прогрес", state=None)
    dp.register_message_handler(process_rating, text="🏆Рейтинг", state="*")
    dp.register_message_handler(process_sos, text="▶️🆘◀️", state=None)
