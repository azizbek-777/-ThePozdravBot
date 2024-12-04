from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from lang.messages import MESSAGES
from loader import dp, db
from .callback_reminder_my_group import create_group_keyboard

@dp.callback_query_handler(Text(startswith=['onReminder', 'offReminder']))
async def on_off_reminder_in_group(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await callback_query.answer()

    # Extract group and reminder IDs from callback data
    group_id, rg_id = map(int, callback_query.data.split(":")[1:3])
    user_id = callback_query.from_user.id

    # Determine the reminder action based on callback data
    is_on = callback_query.data.startswith("onReminder")
    reminder_status = MESSAGES[locale]['reminder_on'] if is_on else MESSAGES[locale]['reminder_off']
    action_text = MESSAGES[locale]["disable_notifications"] if is_on else MESSAGES[locale]["enable_notifications"]

    # Update reminder status in the database
    await db.my_reminder_group_on(user_id, group_id, is_on)

    # Create the updated keyboard
    new_keyboard = create_group_keyboard(is_on, group_id, rg_id, locale)

    # Only update message if keyboard or reminder status changes
    if callback_query.message.reply_markup != new_keyboard:
        group = await dp.bot.get_chat(group_id)
        text = MESSAGES[locale]['reminder_my_group_info'].format(
            group.title, reminder_status, action_text
        )
        await callback_query.message.edit_text(text, reply_markup=new_keyboard)
