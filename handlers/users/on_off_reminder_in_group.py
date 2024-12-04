from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext


from loader import dp, db
from .callback_reminder_my_group import create_group_keyboard

@dp.callback_query_handler(Text(startswith=['onReminder', 'offReminder']))
async def on_off_reminder_in_group(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await callback_query.answer()
    group_id = int(callback_query.data.split(":")[1])
    rg_id = int(callback_query.data.split(":")[2])
    user_id = callback_query.from_user.id
    if callback_query.data.startswith("onReminder"):
        await db.my_reminder_group_on(user_id, group_id, True)
        new_keyboard  = create_group_keyboard(True, group_id, rg_id, locale)
    else:
        await db.my_reminder_group_on(user_id, group_id, False)
        new_keyboard  = create_group_keyboard(False, group_id, rg_id, locale)  # False bilan yarating
    current_markup = callback_query.message.reply_markup
    if current_markup != new_keyboard:
        await callback_query.message.edit_reply_markup(reply_markup=new_keyboard)
    
    