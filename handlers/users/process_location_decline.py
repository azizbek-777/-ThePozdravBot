from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from utils.misc import add_group_message

@dp.message_handler(text="Не хочу")
async def process_location_decline(message: Message):
    text = "Ваш день рождения сохранен, и ваша таймзона установлена по умолчанию (GMT+5). Теперь я буду напоминать о вашем дне рождения в нужное время."
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await add_group_message(message, dp)