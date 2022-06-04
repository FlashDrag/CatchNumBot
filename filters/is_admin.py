from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from config import ADMINS_ID



class IsAdmin(BoundFilter):

    async def check(self, message: Message):
        return message.from_user.id in ADMINS_ID


"""
class IsAdminFilter(BoundFilter):

    # Проверяет, есть ли юзер в списке админов. Список админов в config.ADMINS_ID

    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin() == self.is_admin
"""