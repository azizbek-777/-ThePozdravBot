from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lang.messages import MESSAGES

async def my_groups_keyboard(groups, dp, locale):
    keyboard = InlineKeyboardMarkup()
    for id, group_id, _ in groups:
        group = await dp.bot.get_chat(group_id)
        keyboard.add(InlineKeyboardButton(text=group.title, callback_data=f"reminder_my_group_id:{id}"))
    keyboard.add(
        InlineKeyboardButton(text=MESSAGES[locale]['back'], callback_data="main_menu"),
    )
    return keyboard
