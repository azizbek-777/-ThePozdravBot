import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandPrivacy
import base64

from keyboards.inline import languages_keyboard
from loader import dp, db, bot
from data.config import ADMINS


@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message):
    if message.text != '/start':
        state = message.text.split(' ')[-1]
        decode_state = base64.b64decode(state).decode('utf-8')
        key, chat_id = decode_state.split(':')
        if key == 'addbirthday':
            get_reminder_group = await db.reminder_group_exists(int(chat_id), message.from_user.id)
            if not get_reminder_group:
                await db.add_reminder_group(int(chat_id), message.from_user.id)
                birthday = await db.get_user_birthday(message.from_user.id)
                if birthday:
                    await message.answer("Gruppaga tuwilgan kun qosildi")
     
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
        count = await db.count_users()
        msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
        text = "Выберите язык, на котором хотите использовать бота [ru]\n\n"\
            "Botdan foydalanmoqchi bo'lgan tilni tanlang [uz]\n\n"\
            "Bottan paydalanbaqshı bolǵan tildi saylań [kaa]"
        await message.answer(text, reply_markup=languages_keyboard('set'))
        return
    except asyncpg.exceptions.UniqueViolationError:
        pass
    

    text = "Выберите язык, на котором хотите использовать бота [ru]\n\n"\
        "Botdan foydalanmoqchi bo'lgan tilni tanlang [uz]\n\n"\
        "Bottan paydalanbaqshı bolǵan tildi saylań [kaa]"
    await message.answer(text, reply_markup=languages_keyboard('set'))
    
    