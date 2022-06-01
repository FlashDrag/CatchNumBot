from loader import bot, dp, db
from aiogram.types import CallbackQuery


@dp.callback_query_handler(text='watch')  # if cb.user_data == 'no'
@dp.callback_query_handler(text='close')  # if cb.user_data == 'yes'
async def inline_kb_answer_callback_handler(query: CallbackQuery):
    answer_data = query.data
     # always answer callback queries, even if you have nothing to say
    if answer_data == 'watch':
        # получаем bug_text с базы по глобальной переменной юзера который отправил bug_message
        from handlers.user.user_bug import user_id_bag_message
        bug_text = db.get_bug_text(user_id_bag_message)
        await bot.send_message(query.from_user.id, bug_text[0])
        await query.answer()
    elif answer_data == "close":
        await bot.send_message(query.from_user.id, 'Ok')
        await query.answer(f"Покасики 😜")