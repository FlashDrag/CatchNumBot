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

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in config.ADMINS_ID
"""