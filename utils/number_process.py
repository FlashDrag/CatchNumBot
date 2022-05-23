from math import ceil, log2
from  random import randint
from keyboards.inline_markup import start_inline_markup
from loader import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

dic = {1:"🥇", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "останньої😓"}

# States
class reg(StatesGroup):
    # st_name = State()
    # st_max_num = State()
    # st_random_num = State() 
    st_number = State() 
    # st_attempt = State()
    # st_user_attempt = State()
    # st_win = State()


async def process_start_button(message: types.Message,  state: FSMContext):
    # query = message
    async with state.proxy() as user_data:
        user_data.setdefault('max_num', 10)
    user_data = await state.get_data()   
    await state.update_data(random_num=randint(1, user_data['max_num']))
    await state.update_data(attempt=ceil(log2(user_data['max_num'])))
    # модуль math вычисляет минимальное к-ство попыток для угадывания нашего числа
    await reg.st_number.set()
    user_data = await state.get_data() # получаем со словаря обновленные значения
    print(user_data)
    await bot.send_message(message.from_user.id, f"Поїхали! Вгайдай число від 1️⃣ до {user_data['max_num']}", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, f"В тебе є {user_data['attempt']} спроб")
    # await print(f"Random num for {user_data['name']} is {user_data['random_num']}")


async def process_start(query: types.CallbackQuery, state: FSMContext):
    # query = message
    async with state.proxy() as user_data:
        user_data.setdefault('max_num', 10)
    user_data = await state.get_data()   
    await state.update_data(random_num=randint(1, user_data['max_num']))
    await state.update_data(attempt=ceil(log2(user_data['max_num'])))
    # модуль math вычисляет минимальное к-ство попыток для угадывания нашего числа
    await reg.st_number.set()
    user_data = await state.get_data() # получаем со словаря обновленные значения
    print(user_data)
    # await query.message.edit_text()
    await query.answer(f"В тебе є {user_data['attempt']} спроб", show_alert=True)
    await query.message.delete()
    await bot.send_message(query.from_user.id, f"Поїхали! Вгайдай число від 1️⃣ до {user_data['max_num']}", reply_markup=types.ReplyKeyboardRemove())
    # await print(f"Random num for {user_data['user_name']} is {user_data['random_num']}")


async def is_valid(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.isdigit() and int(message.text) in range(1, user_data['max_num'] + 1):
        await guess(message, state)
    else:
        await message.reply('💩💩💩')
        return await bot.send_message(message.from_user.id, "Число повинно бути від 1 до " + str(user_data['max_num']) + ". Спробуй ще раз")


async def guess(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(number=int(message.text))
    user_data.setdefault('user_attempt', 0)
    await state.update_data(user_attempt=user_data["user_attempt"] + 1)
    user_data = await state.get_data()
    if user_data['number'] != user_data['random_num']:
        await message.reply(f"Залишилось спроб: {user_data['attempt'] - user_data['user_attempt']}")
    if user_data['user_attempt'] == user_data['attempt'] and user_data['number'] != user_data['random_num']:
        await state.finish()
        await bot.send_message(message.from_user.id, 'Спроби закінчилися😩  Ти програв 💩😹')
        question = f'Спробуєш підкорити цифри ще раз?'
        await bot.send_message(message.from_user.id, text=question, reply_markup=start_inline_markup())
    else:
        if user_data['number'] < user_data['random_num']:
            return await bot.send_message(message.from_user.id, 'Замало. Спробуй щось побільше')
        elif user_data['number'] > user_data['random_num']:
            return await bot.send_message(message.from_user.id, 'Забагато. Спробуй щось поменше')
        else:
            user_data = await state.get_data()
            await message.reply(f'В яблучко 🎯    Вітаю❗️')
            try:
                await bot.send_message(message.from_user.id, f"З {dic[user_data['user_attempt']]} - ї спроби  👏")
            except KeyError:
                await bot.send_message(message.from_user.id, f"З {user_data['user_attempt']}-ї спроби  👏")
            user_data.setdefault('win', 0)
            await state.update_data(max_num=user_data['max_num'] * 2)
            await state.update_data(win=user_data['win'] + 1)
            await state.update_data(user_attempt=0)
            user_data = await state.get_data()
            await bot.send_message(message.from_user.id, f"Рівень №{user_data['win']} в діапазоні {int(user_data['max_num'] / 2)} підкорено!")
            await state.reset_state(with_data=False)
            '''
            BotDB.add_record(user_name, max_num, win)
            users[user_data["user_name"]] = user_data['win']
            '''
            # print(f"Raiting {users}")
            question = f'Наступний рівень?'
            await bot.send_message(message.from_user.id, text=question, reply_markup=start_inline_markup()) 
            #вопрос и inline-клавиатура для ответа "reply_markup=gen_markup()" 


def register_handlers_num_process(dp: Dispatcher):
    dp.register_message_handler(is_valid, state=reg.st_number)