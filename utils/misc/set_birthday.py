from aiogram.types import Message

from keyboards.inline import generate_years_keyboard

async def set_birthday(message: Message, year: int = 2001):
    text = "Выберите год вашего рождения:"
    await message.answer(text, reply_markup=generate_years_keyboard(year)) 