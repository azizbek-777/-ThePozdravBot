from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import main_btn
from lang.messages import MESSAGES
from loader import dp

@dp.callback_query_handler(text="main_menu")
async def handle_birthday_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]['welcome'].format(callback_query.from_user.full_name)
    bot = await dp.bot.get_me()
    keyboard = main_btn(bot.username, locale)
    await callback_query.message.answer(text, disable_web_page_preview=True, reply_markup=keyboard)
    