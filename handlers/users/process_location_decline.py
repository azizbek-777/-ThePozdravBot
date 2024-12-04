from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from lang.messages import MESSAGES
from loader import dp, db
from utils.misc import add_group_message

@dp.message_handler(text=["Не хочу", "Yuborishni xohlamayman", "Jibere almayman"])
async def process_location_decline(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    group_id = data.get("add_birthday_group_id")
    if group_id:
        group = await dp.bot.get_chat(group_id)
        get_reminder_group = await db.reminder_group_exists(int(group_id), message.from_user.id)
        if get_reminder_group is None:
            await db.add_reminder_group(int(group_id), message.from_user.id)
        text =  MESSAGES[locale]["birthday_added_to_group"].format(group_id, group.title)
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    text = MESSAGES[locale]["birthday_timezone_set"]
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await add_group_message(message, dp, locale)