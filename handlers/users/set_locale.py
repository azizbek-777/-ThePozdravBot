from aiogram.types import CallbackQuery

from loader import dp, db
from utils.misc import set_birthday, add_group_message

@dp.callback_query_handler(text_contains="language")
async def set_locale(callback_query: CallbackQuery):
    await callback_query.message.delete()
    locale = callback_query.data.split(":")[1]
    method = callback_query.data.split(":")[2]
    await db.set_user_locale(locale, callback_query.from_user.id)
    if method == "set":    
        text = f"Привет, <a href='tg://user?id={callback_query.from_user.id}'>{callback_query.from_user.full_name}</a>!\n" \
        "Я помогу напомнить вашей группе о вашем дне рождения. Пользуясь ботом, вы соглашаетесь с нашим <a href='https://telegra.ph/Obrabotka-dannyh-11-29'>пользовательским соглашением</a>"
        await callback_query.message.answer(text, disable_web_page_preview=True)
        
        birthday = await db.get_user_birthday(callback_query.from_user.id)
        if birthday is None:
            await set_birthday(callback_query.message)
            return
        
        await add_group_message(callback_query.message, dp)
        return
         
    if method == "update":
        text = "Bot tili tabıslı ózgerdi !\nBottan paydalanıwdı dawam ettiriwińiz múmkin"
        await callback_query.message.answer(text)