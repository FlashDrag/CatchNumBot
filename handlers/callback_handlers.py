from keyboards.keyboard_markup import sos_menu_markup
from loader import dp, bot
from utils.number_process import process_start
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.keyboard_markup import sos_menu_markup, main_start_menu_markup

@dp.callback_query_handler(text='niz') 
async def help_inline_markup_callback_handler(query: CallbackQuery, state: FSMContext):
    answer_data = query.data
    if answer_data == 'niz':
        await query.answer("Пояснюю:\nКожен раз ділимо на 2 діапазон, що залишився", show_alert=True)
     # always answer callback queries, even if you have nothing to say
        await query.message.delete()
        await bot.send_message(query.from_user.id, "Дойшло? Круто! Нажми старт, щоб почати")
        await bot.send_message(query.from_user.id, "Досі у ваукумі? SOS -  для зв'язку з адміном. Не соромся)", reply_markup=sos_menu_markup())
        await state.reset_state(with_data=False)



# Use multiple registrators. Handler will execute when one of the filters is OK
@dp.callback_query_handler(text='no')  # if cb.user_data == 'no'
@dp.callback_query_handler(text='yes')  # if cb.user_data == 'yes'
async def inline_kb_answer_callback_handler(query: CallbackQuery, state: FSMContext):
    answer_data = query.data
     # always answer callback queries, even if you have nothing to say
    if answer_data == 'yes':
        await process_start(query, state)
    elif answer_data == "no":
        await bot.send_message(query.from_user.id, 'Лади, коли надумаєш зіргати введи слово СТАРТ ⬇️⏺', reply_markup=main_start_menu_markup())
        await query.answer(f"Покасики 😜", show_alert=True)
        await query.message.delete()
        await state.reset_state(with_data=False)