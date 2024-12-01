import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import base64

from keyboards.inline import languages_keyboard
from loader import dp, db, bot
from data.config import ADMINS


@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message):
    try:
        # Add new user to the database and get the user count
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
        count = await db.count_users()
        
        # Notify admins about the new user added
        msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
        
        # Send language selection message
        text = (
            "Выберите язык, на котором хотите использовать бота [ru]\n\n"
            "Botdan foydalanmoqchi bo'lgan tilni tanlang [uz]\n\n"
            "Bottan paydalanbaqshı bolǵan tildi saylań [kaa]"
        )
        await message.answer(text, reply_markup=languages_keyboard('set'))
    
    except asyncpg.exceptions.UniqueViolationError:
        # Handle user already exists in the database
        pass
    
    # Process state data for adding birthday reminders if available
    state_data = message.text.split(' ')
    if len(state_data) > 1:
        state = state_data[-1]
        try:
            # Decode the base64 state and check for valid keys
            decode_state = base64.b64decode(state).decode('utf-8')
            key, chat_id = decode_state.split(':')
            
            if key == 'addbirthday':
                # Check if reminder group exists, otherwise create it
                get_reminder_group = await db.reminder_group_exists(int(chat_id), message.from_user.id)
                if not get_reminder_group:
                    await db.add_reminder_group(int(chat_id), message.from_user.id)
                    birthday = await db.get_user_birthday(message.from_user.id)
                    
                    if birthday:
                        # Notify user of successful birthday reminder setup
                        group = await bot.get_chat(int(chat_id))
                        text = (
                            f"✅ Ваш день рождения успешно добавлен в группу “<a href='tg://user?id={chat_id}'>{group.title}</a>”\n\n"
                            "Теперь в день вашего рождения в группу будет отправляться сообщение с напоминанием.\n\n"
                            "Чтобы управлять напоминаниями в группах, отправьте /my_groups"
                        )
                        await message.answer(text)
                        return
        except (base64.binascii.Error, ValueError) as e:
            # Log error if base64 decode or split fails
            print(f"Error decoding state: {e}")
            
    # If no valid state, resend language selection message
    await message.answer(
        "Выберите язык, на котором хотите использовать бота [ru]\n\n"
        "Botdan foydalanmoqchi bo'lgan tilni tanlang [uz]\n\n"
        "Bottan paydalanbaqshı bolǵan tildi saylań [kaa]",
        reply_markup=languages_keyboard('set')
    )
