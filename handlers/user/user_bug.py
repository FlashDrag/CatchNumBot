from states.states import Bug
from loader import bot, dp, db
from keyboards.user_markup.keyboard_markup import start_menu_markup
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.admin_markup.inline_markup import admin_bug_inline_markup
from config import ADMINS_ID as ad_id


async def get_bug_message(message: types.Message):
    await bot.send_message(message.from_user.id, f'Опиши свою проблему чи пропозицію в декількох словах та відправ цьому боту зараз', reply_markup=start_menu_markup())
    await Bug.get_bug.set()


async def process_bug_message(message: types.Message, state: FSMContext):
    global user_id_bag_message
    if len(message.text) > 160:
        await bot.send_message(message.from_user.id, f'''Слишком длинное сообщение - {len(message.text)}.
        Максимум 160 символов''')
        return
    else:
        user_id_bag_message = message.from_user.id
        if message.chat.first_name:
            name = message.chat.first_name
        else:
            name = message.chat.username
        # сохраняем жалобу юзера в базу
        db.set_bug_message(message)
        # сообщение админу со ссылкой на юзера (tg://user?id={user_id}) и кнопкой посмотреть сообщение с базы
        await bot.send_message(ad_id['Pasha'], f'Новое bug_сообщение от ▶️<a href="tg://user?id={user_id_bag_message}">{name}</a>◀️\n '
                                                'Просмотреть?', reply_markup=admin_bug_inline_markup())
        await bot.send_message(message.from_user.id, f'📩Спасибо за обратную связь!', reply_markup=start_menu_markup())
        await state.reset_state(with_data=False)


def register_handlers_user_bug(dp: Dispatcher):
    dp.register_message_handler(get_bug_message, commands="bug", state="*")
    dp.register_message_handler(process_bug_message, content_types=["text"], state=Bug.get_bug)