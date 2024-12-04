from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from keyboards.inline import my_groups_keyboard, main_menu_keyboard
from lang.messages import MESSAGES
from loader import dp, db

@dp.callback_query_handler(text='my_groups')
async def bot_my_groups_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]["select_group"]
    groups = await db.my_reminder_groups(callback.from_user.id)
    
    keyboard = await my_groups_keyboard(groups, dp, locale)
    await callback.message.answer(text, reply_markup=keyboard)