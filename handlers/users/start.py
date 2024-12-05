import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
import base64

from keyboards.inline import languages_keyboard, main_btn
from keyboards.inline.years_btn import generate_years_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from data.config import ADMINS


@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    state_data = message.text.split(' ')
    
    try:
        # Add new user to the database and get the user count
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
        count = await db.count_users()
        
        # Notify admins about the new user added
        msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await dp.bot.send_message(chat_id=ADMINS[0], text=msg)
        await message.answer(
        "Выберите язык, на котором хотите использовать бота [ru]\n\n"
        "Botdan foydalanmoqchi bo'lgan tilni tanlang [uz]\n\n"
        "Bottan paydalanbaqshı bolǵan tildi saylań [kaa]",
        reply_markup=languages_keyboard('set')
        )
        if len(state_data) > 1:
            state_d = state_data[-1]
            decode_state = base64.b64decode(state_d).decode('utf-8')
            key, chat_id = decode_state.split(':')
            await state.update_data(add_birthday_group_id=chat_id)
        return
    except asyncpg.exceptions.UniqueViolationError:
        # Handle user already exists in the database
        pass
    
    # Process state data for adding birthday reminders if available
    if len(state_data) > 1:
        state_d = state_data[-1]
        try:
            # Decode the base64 state and check for valid keys
            decode_state = base64.b64decode(state_d).decode('utf-8')
            key, chat_id = decode_state.split(':')
            
            if key == 'addbirthday':
                birthday = await db.get_user_birthday(message.from_user.id)
                # Check if reminder group exists, otherwise create it
                get_reminder_group = await db.reminder_group_exists(int(chat_id), message.from_user.id)
                if get_reminder_group is None:
                    await db.add_reminder_group(int(chat_id), message.from_user.id)
            if birthday:
                group = await dp.bot.get_chat(chat_id)
                text = MESSAGES[locale]["birthday_added_to_group"].format(chat_id, group.title)
                await message.answer(text)
            else:
                text = MESSAGES[locale]["select_birth_year"]
                await message.answer(text, reply_markup=generate_years_keyboard(2001)) 
                return
        except (base64.binascii.Error, ValueError) as e:
            print(f"Error decoding state: {e}")
    
    username = message.from_user.username
    if username is None:
        username = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
    
    text = MESSAGES[locale]['welcome'].format(message.from_user.full_name)
    bot = await dp.bot.get_me()
    keyboard = main_btn(bot.username, locale)
    await message.answer(text, disable_web_page_preview=True, reply_markup=keyboard)