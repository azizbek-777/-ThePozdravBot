from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text

from loader import dp, db
from .callback_reminder_my_group import create_group_keyboard

@dp.callback_query_handler(Text(startswith=['onReminder', 'offReminder']))
async def on_off_reminder_in_group(callback_query: CallbackQuery):
    await callback_query.answer()
    group_id = int(callback_query.data.split(":")[1])
    user_id = callback_query.from_user.id
    if callback_query.data.startswith("onReminder"):
        await db.my_reminder_group_on(user_id, group_id, True)
        keyboard = create_group_keyboard(True, group_id)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        await db.my_reminder_group_on(user_id, group_id, False)
        keyboard = create_group_keyboard(False, group_id)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    
    