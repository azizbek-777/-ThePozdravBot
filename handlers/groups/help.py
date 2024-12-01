from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

@dp.message_handler(CommandHelp(), chat_type="group")
async def bot_help_group(message: Message):
    text = """
/list_birthday - Список день рождения участников группы
/add - Добавить свой день рождения
/language - Изменение языка бота    
"""
    await message.reply(text)
