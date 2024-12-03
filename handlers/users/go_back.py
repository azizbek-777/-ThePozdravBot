from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards.inline import my_groups_keyboard
from lang.messages import MESSAGES
from loader import dp, db

@dp.callback_query_handler(text="go_back")
async def go_back(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]["select_group"]
    groups = await db.my_reminder_groups(callback_query.from_user.id)
    keyboard = await my_groups_keyboard(groups, dp)
    await callback_query.message.edit_text(text, reply_markup=keyboard)