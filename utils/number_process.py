from math import ceil, log2
from  random import randint
from keyboards.user_markup.inline_markup import start_inline_markup
from loader import dp, bot, db
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from states.states import Num
import logging
import logging.config

logging.config.fileConfig('logging/logging.conf',
                        disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# from aiogram.utils.exceptions import MessageCantBeEdited
# except MessageCantBeEdited as e:

dic = {1:"🥇", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}

async def process_start_button(message: types.Message,  state: FSMContext):
    user_id = message.from_user.id
    db.update_start_game_count(user_id)  #счетчик
    async with state.proxy() as data:
        # max_num получаем с основной БД и заносим в словарь 'data' (FSM - машины состояний)
        data['max_num'] = db.get_max_num(user_id)
        # Устанавливаем значения в словаре 'data' в отношении к max_num
        data['user_attempt'] = 0
        data['random_num'] = randint(1, data['max_num'])
        data['attempt'] = ceil(log2(data['max_num']))
    # модуль math вычисляет минимальное к-ство попыток для угадывания нашего числа
    await Num.st_number.set()
    logger.info(f'start:{data}')
    text = f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n "\
            f"<b>Поїхали! Вгайдай число від 1️⃣ до {data['max_num']}</b>\n "\
            f"⚠️В тебе є {data['attempt']} спроб"
    await bot.send_message(message.from_user.id, text, reply_markup=types.ReplyKeyboardRemove())
    # await logger.debug(f"Random num for {data['name']} is {data['random_num']}")

async def process_start_query(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    db.update_start_game_count(user_id)  #счетчик
    async with state.proxy() as data:
        # max_num получаем с основной БД и заносим в словарь 'data' (FSM - машины состояний)
        data['max_num'] = db.get_max_num(user_id)
        # Устанавливаем значения в словаре 'data' в отношении к max_num
        data['user_attempt'] = 0
        data['random_num'] = randint(1, data['max_num'])
        data['attempt'] = ceil(log2(data['max_num']))
    # модуль math вычисляет минимальное к-ство попыток для угадывания нашего числаа
    await Num.st_number.set()
    logger.info(f'start:{data}')
    # await query.message.edit_text()
    await query.answer(f"В тебе є {data['attempt']} спроб", show_alert=True)
    text = f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n "\
            f"<b>Поїхали! Вгайдай число від 1️⃣ до {data['max_num']}</b>"
    await bot.send_message(query.from_user.id, text, reply_markup=types.ReplyKeyboardRemove())
    # await logger.debug(f"Random num for {data['user_name']} is {data['random_num']}")

async def is_valid(message: types.Message, state: FSMContext):
    async with state.proxy() as data: 
        if message.text.isdigit() and int(message.text) in range(1, data['max_num'] + 1):
            await process_num(message, state)
        else:
            await message.reply('💩💩💩')
            await bot.send_message(message.from_user.id, f"Число повинно бути від 1 до {data['max_num']}. Спробуй ще раз")
            return

async def process_num(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.from_user.id
        data['number'] = int(message.text)
        data['user_attempt'] += 1
    if data['number'] != data['random_num']:
        await message.reply(f"Залишилось спроб: {data['attempt'] - data['user_attempt']}")
    if data['user_attempt'] == data['attempt'] and data['number'] != data['random_num']:
        # сброс данных
        db.reset_values(user_id)
        db.update_game_over_count(user_id)
        db.update_last_over_date(user_id)
        await state.finish()

        await bot.send_message(user_id, 'Спроби закінчилися😩  Ти програв 💩😹')
        question = f'Спробуєш підкорити цифри ще раз?'
        await bot.send_message(user_id, text=question, reply_markup=start_inline_markup())
    else:
        if data['number'] < data['random_num']:
            return await bot.send_message(user_id, 'Замало. Спробуй щось побільше')
        elif data['number'] > data['random_num']:
            return await bot.send_message(user_id, 'Забагато. Спробуй щось поменше')
        else:
            # обновляем данные в основной БД
            db.update_max_num(user_id)
            db.update_win_count(user_id)
            db.update_win_count_for_stat(user_id)
            db.update_last_win_date(user_id)
            # получаем данные с БД
            win_count = db.get_win_count(user_id)
            max_num = db.get_max_num(user_id)
            max_num_for_stat = db.get_max_num_for_stat(user_id)
            # обновляем максимальное число юзера в основной БД, если последнее 'max_num' больше 'max_num_for_stat' которое в основной БД
            db.update_max_num_for_stat(user_id, max_num) if max_num > max_num_for_stat else None
            logger.info(f'finish:{data}')

            try:
                await message.reply(f"Перемога🎯\n З {dic[data['user_attempt']]} - ї спроби  👏")
            except KeyError:
                await message.reply(f"Перемога🎯\n З {data['user_attempt']}-ї спроби  👏")
            await bot.send_message(user_id, f"Рівень №{win_count} в діапазоні {int(max_num / 2)} підкорено!\n "
                                            "Наступний рівень❓❔❓", reply_markup=start_inline_markup()) 
            await state.reset_state(with_data=False)         
            await state.update_data(user_attempt=0)
            #вопрос и inline-клавиатура для ответа "reply_markup=gen_markup()" 


def register_handlers_num_process(dp: Dispatcher):
    dp.register_message_handler(is_valid, state=Num.st_number)