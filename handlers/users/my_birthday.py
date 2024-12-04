from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime

from keyboards.inline import edit_birthday_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from utils.misc import set_birthday

@dp.message_handler(commands=["my_birthday"], chat_type="private")
async def handle_birthday_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    user_id = message.from_user.id
    
    birthday = await db.get_user_birthday(user_id)
    
    if not birthday:
        await set_birthday(message, locale=locale)
        return
    # Prepare birth date and current date
    birth_date = datetime.combine(birthday, datetime.min.time())
    current_date = datetime.now()
    current_year = current_date.year

    # Calculate the next birthday and time differences
    next_birthday = birth_date.replace(year=current_year)
    if next_birthday < current_date:
        next_birthday = next_birthday.replace(year=current_year + 1)
    
    days_until = (next_birthday - current_date).days
    days_since = (current_date - next_birthday.replace(year=next_birthday.year - 1)).days

    text = (
        MESSAGES[locale]["your_birthday"].format(birth_date.strftime('%d.%m.%Y')) +
        "\n\n" + MESSAGES[locale]["your_birthday_in"].format(days_until) +
        "\n" + MESSAGES[locale]["your_birthday_ago"].format(days_since)
    )
    
    await message.answer(text, reply_markup=edit_birthday_keyboard(locale))
