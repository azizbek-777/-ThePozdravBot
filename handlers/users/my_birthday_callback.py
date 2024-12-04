from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from keyboards.inline import edit_birthday_keyboard, main_menu_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from utils.misc import set_birthday

@dp.callback_query_handler(text="my_birthday")
async def handle_birthday_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    data = await state.get_data()
    locale = data.get("locale", "ru")
    user_id = callback_query.from_user.id
    
    birthday = await db.get_user_birthday(user_id)
    
    if not birthday:
        await set_birthday(callback_query.message, locale=locale)
        return
    
    text = MESSAGES[locale]["your_birthday"].format(birthday)
    keyboard = edit_birthday_keyboard(locale)
    await callback_query.message.answer(text, reply_markup=keyboard)
    