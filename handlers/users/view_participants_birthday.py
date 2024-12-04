from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from datetime import datetime
from aiogram.dispatcher import FSMContext

from lang.messages import MESSAGES
from loader import dp, db


@dp.callback_query_handler(Text(startswith=['view_participants_birthday']))
async def view_participants_birthday(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    group_id = int(callback_query.data.split(":")[1])
    rg_id = int(callback_query.data.split(":")[2])
    data = await db.get_reminder_groups_with_users_where_group_id(group_id)
    
    group = await dp.bot.get_chat(group_id)
    
    text = MESSAGES[locale]["birthday_list_group"].format(group.title)
    i = 1
    for _, user_id, birthday, _ in data:
        user = await dp.bot.get_chat(user_id)

        date_obj = datetime.strptime(str(birthday), "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.month
        
        formatted_date = f"{day} {MESSAGES[locale]['months'][month - 1]}"
        
        text += MESSAGES[locale]["birthday_list_item"].format(i, user.id, user.full_name, formatted_date)
        i += 1
    back_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=MESSAGES[locale]["back"], callback_data=f"reminder_my_group_id:{rg_id}")
    )
    
    await callback_query.message.edit_text(text, reply_markup=back_button)


    