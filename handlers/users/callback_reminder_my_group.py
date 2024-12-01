from aiogram.types import CallbackQuery
from loader import dp, db

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Create the inline keyboard
def create_group_keyboard(is_reminder_on: bool):
    # Define buttons based on reminder status
    add_birthday_button = InlineKeyboardButton(
        text="✅ Добавить день рождения" if not is_reminder_on else "🚫 Удалить день рождения",
        callback_data="add_birthday" if not is_reminder_on else "remove_birthday"
    )
    participants_button = InlineKeyboardButton(text="👥 Участники", callback_data="view_participants")
    back_button = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")

    # Create the keyboard layout
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(add_birthday_button, participants_button, back_button)

    return keyboard

@dp.callback_query_handler(text_contains="reminder_my_group_id:")
async def callback_reminder_my_group(callback_query: CallbackQuery):
    await callback_query.answer()
    
    # Extract the group ID from the callback data
    rg_id = callback_query.data.split(':')[1]
    
    # Fetch reminder group data from the database
    my_reminder_group = await db.get_reminder_my_group(int(rg_id), callback_query.from_user.id)
    
    # If no group data found, return early to avoid errors
    if not my_reminder_group:
        await callback_query.message.edit_text("Ошибка: Напоминание не найдено для вашей группы.", parse_mode="markdown")
        return
    
    # Get the group information
    group = await dp.bot.get_chat(my_reminder_group[0]['group_id'])
    
    # Determine notification status message
    reminder_status = "✅ Включено" if my_reminder_group[0]['is_reminder_on'] else "🚫 Отключено"
    action_text = (
        "Чтобы отключить уведомления и удалить день рождения из этой группы, нажмите на кнопку “🚫 Удалить”"
        if my_reminder_group[0]['is_reminder_on']
        else "Чтобы включить уведомления и добавить день рождения в эту группу, нажмите на кнопку “✅ Добавить день рождения”"
    )

    # Prepare the response message
    text = f"""
Название группы: “*{group.title}*”

*Уведомление: {reminder_status}*
{action_text}

Чтобы посмотреть день рождения участников, нажмите на кнопку “Участники”
    """
    
    # Edit the message with the new text
    await callback_query.message.edit_text(text, parse_mode="markdown", reply_markup=create_group_keyboard(my_reminder_group[0]['is_reminder_on']))
