from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from lang.messages import MESSAGES
from loader import dp
from utils.misc import add_group_message

@dp.message_handler(text=["Не хочу", "Yuborishni xohlamayman", "Jibere almayman"])
async def process_location_decline(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]["birthday_timezone_set"]
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await add_group_message(message, dp, locale)