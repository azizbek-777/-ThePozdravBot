from aiogram.types import Message

from keyboards.inline import add_group_keyboard
from lang.messages import MESSAGES

async def add_group_message(message: Message, dp, locale):
    bot = await dp.bot.get_me()
    text = MESSAGES[locale]["add_group"]
    await message.answer(
        text,
        reply_markup=add_group_keyboard(bot.username, locale)
    )