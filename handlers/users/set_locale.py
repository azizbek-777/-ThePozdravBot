from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from lang import MESSAGES
from loader import dp, db
from utils.misc import set_birthday, add_group_message

@dp.callback_query_handler(text_contains="language")
async def set_locale(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    locale = callback_query.data.split(":")[1]
    await state.update_data(locale=locale)
    method = callback_query.data.split(":")[2]
    await db.set_user_locale(locale, callback_query.from_user.id)
    if method == "set":    
        text = MESSAGES[locale]['hello'].format(callback_query.from_user.id, callback_query.from_user.full_name)
        await callback_query.message.answer(text, disable_web_page_preview=True)
        
        birthday = await db.get_user_birthday(callback_query.from_user.id)
        if birthday is None:
            await set_birthday(callback_query.message, locale=locale)
            return
        
        await add_group_message(callback_query.message, dp, locale)
        return
         
    if method == "update":
        text = MESSAGES[locale]['language_changed']
        await callback_query.message.answer(text)