from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from lang.messages import MESSAGES
from loader import dp
from utils.misc.send_add_birthday_message import send_birthday_message

@dp.message_handler(CommandStart(), chat_type=["group", "supergroup"])
async def bot_start_group(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    bot = await dp.bot.get_me()
    await send_birthday_message(message, bot.username, locale)

