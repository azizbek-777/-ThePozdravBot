from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext

from lang.messages import MESSAGES
from loader import dp

@dp.message_handler(CommandHelp(), chat_type="private")
async def bot_help(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]["help_command"]
    await message.reply(text)