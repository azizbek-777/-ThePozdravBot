from aiogram.types import Message

from keyboards.inline import generate_years_keyboard
from lang.messages import MESSAGES

async def set_birthday(message: Message, year: int = 2001, locale: str = "ru"):
    text = MESSAGES[locale]["select_birth_year"]
    await message.answer(text, reply_markup=generate_years_keyboard(year)) 