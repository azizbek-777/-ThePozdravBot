from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def my_groups_keyboard(groups, dp):
    keyboard = InlineKeyboardMarkup()
    for id, group_id, _ in groups:
        group = await dp.bot.get_chat(group_id)
        keyboard.add(InlineKeyboardButton(text=group.title, callback_data=f"reminder_group_id:{id}"))
    return keyboard
