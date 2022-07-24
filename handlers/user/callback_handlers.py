from keyboards.user_markup.keyboard_markup import sos_menu_markup
from loader import dp, bot, db
from utils.number_process import process_start_query
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.user_markup.keyboard_markup import sos_menu_markup, main_start_menu_markup


@dp.callback_query_handler(text='niz')
async def help_inline_markup_callback_handler(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    db.update_pidkazka_count(user_id)  # счетчик
    answer_data = query.data
    await query.answer("Кожен раз ділимо на 2 діапазон, що залишився", show_alert=True)
    # always answer callback queries, even if you have nothing to say
    await bot.send_message(query.from_user.id, "Зрозуміло? Круто! Тисни старт, щоб почати\n\n "
                                               "Досі у ваукумі? ➡️SOS⬅️ -  для зв'язку з адміном.",
                                               reply_markup=sos_menu_markup())
    await state.reset_state(with_data=False)


# Use multiple registrators. Handler will execute when one of the filters is OK
@dp.callback_query_handler(text='no')  # if cb.user_data == 'no'
@dp.callback_query_handler(text='yes')  # if cb.user_data == 'yes'
async def inline_kb_answer_callback_handler(query: CallbackQuery, state: FSMContext):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    if answer_data == 'yes':
        await query.message.delete()
        await process_start_query(query, state)
    elif answer_data == "no":
        text = f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n "\
            f"<b>Лади, надумаєш зіграти просто введи слово СТАРТ ⬇️⏺</b> "
        await bot.send_message(query.from_user.id, text, reply_markup=main_start_menu_markup())
        await query.answer(f"Покасики 😜", show_alert=True)
        await query.message.delete()
        await state.reset_state(with_data=False)
