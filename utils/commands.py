from aiogram import Bot
from aiogram.types.bot_command import BotCommand

# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запуск Ігри 👊"),
        BotCommand(command="/progress", description="Мій рівень 💪"),
        BotCommand(command="/help", description="Допомога 🙏"),
        BotCommand(command="/info", description="Інформація"),
        BotCommand(command="/cancel", description="Відміна 🖕")
        # BotCommand(command="/cancel", description="Допомога 🙏")
        ]
    await bot.set_my_commands(commands)


# BotFather
# start - Запуск Ігри 👊
# progress - Мій рівень 💪
# help - Допомога 🙏
# cancel - Відміна 🖕