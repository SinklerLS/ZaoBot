from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


# Не отображать /start для авторизованных пользователей
async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Авторизироваться'
        ),
        BotCommand(
            command='logout',
            description='Выйти из аккаунта'
        ),
        BotCommand(
            command='cancel',
            description='Вернуться в меню'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
