from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    if message.chat.type == "private":
        text = "/language - Изменение языка бота" \
        "/my_birthday - Изменить ili Добавить день рождения\n"
        await message.reply(text)
        return
    
    text = "/list_birthday - Список день рождения участников группы\n" \
        "/my_birthday - Изменить ili Добавить день рождения\n"
    await message.reply(text) 
    
