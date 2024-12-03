from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from lang.messages import MESSAGES
from loader import dp, db

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Create the inline keyboard
def create_group_keyboard(is_reminder_on: bool, group_id, rg_id, locale):
    # Define buttons based on reminder status
    add_birthday_button = InlineKeyboardButton(
        text=MESSAGES[locale]['add_birthday'] if not is_reminder_on else MESSAGES[locale]['delete_birthday'],
        callback_data=f"onReminder:{group_id}" if not is_reminder_on else f"offReminder:{group_id}"
    )
    participants_button = InlineKeyboardButton(text=MESSAGES[locale]['participants'], callback_data=f"view_participants_birthday:{group_id}:{rg_id}")
    back_button = InlineKeyboardButton(text=MESSAGES[locale]['back'], callback_data="go_back")

    # Create the keyboard layout
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(add_birthday_button, participants_button, back_button)

    return keyboard

@dp.callback_query_handler(text_contains="reminder_my_group_id:")
async def callback_reminder_my_group(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = await state.get_data()
    locale = data.get("locale", "ru")
    # Extract the group ID from the callback data
    rg_id = callback_query.data.split(':')[1]
    
    # Fetch reminder group data from the database
    my_reminder_group = await db.get_reminder_my_group(int(rg_id), callback_query.from_user.id)
    
    # If no group data found, return early to avoid errors
    if not my_reminder_group:
        await callback_query.message.edit_text(MESSAGES[locale]['reminder_not_found'], parse_mode="markdown")
        return
    
    # Get the group information
    group = await dp.bot.get_chat(my_reminder_group[0]['group_id'])
    
    # Determine notification status message
    reminder_status = MESSAGES[locale]['reminder_on'] if my_reminder_group[0]['is_reminder_on'] else MESSAGES[locale]['reminder_off']
    action_text = (
        MESSAGES[locale]["disable_notifications"]
        if my_reminder_group[0]['is_reminder_on']
        else MESSAGES[locale]["enable_notifications"]
    )

    text = MESSAGES[locale]['reminder_my_group_info'].format(
        group.title,
        reminder_status,
        action_text
    )    
    await callback_query.message.edit_text(text, parse_mode="html", reply_markup=create_group_keyboard(my_reminder_group[0]['is_reminder_on'], my_reminder_group[0]['group_id'], rg_id, locale))
