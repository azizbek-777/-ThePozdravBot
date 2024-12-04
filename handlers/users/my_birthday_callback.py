from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime

from keyboards.inline import edit_birthday_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from utils.misc import set_birthday

@dp.callback_query_handler(text="my_birthday")
async def handle_birthday_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    
    data = await state.get_data()
    locale = data.get("locale", "ru")
    user_id = callback_query.from_user.id
    
    # Retrieve the user's birth date from the database
    birthday = await db.get_user_birthday(user_id)
    
    if not birthday:  # Correctly check the `birthday` variable
        await set_birthday(callback_query.message, locale=locale)
        return

    # Prepare birth date and current date
    birth_date = datetime.combine(birthday, datetime.min.time())  # Correctly assign the birth date
    current_date = datetime.now()
    current_year = current_date.year

    # Calculate the next birthday and time differences
    next_birthday = birth_date.replace(year=current_year)
    if next_birthday < current_date:
        next_birthday = next_birthday.replace(year=current_year + 1)
    
    days_until = (next_birthday - current_date).days
    days_since = (current_date - next_birthday.replace(year=next_birthday.year - 1)).days

    # Format the response message
    text = (
        MESSAGES[locale]["your_birthday"].format(birth_date.strftime('%d.%m.%Y')) +
        "\n\n" + MESSAGES[locale]["your_birthday_in"].format(days_until) +
        "\n" + MESSAGES[locale]["your_birthday_ago"].format(days_since)
    )
    
    # Send the message with the keyboard
    keyboard = edit_birthday_keyboard(locale)
    await callback_query.message.answer(text, reply_markup=keyboard)
