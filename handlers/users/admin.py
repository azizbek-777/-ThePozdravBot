import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext


from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline import admin_main_btn
from states import StateSendForward, StateSendMessage, ChannelState
from utils.misc.export_excel import export_votes_to_excel


@dp.message_handler(commands='admin', state="*", user_id=ADMINS)
async def commad_admin(message: types.Message, state: FSMContext):
    await state.finish()
    users_count = await db.count_users()
    groups_count = await db.count_groups()
    await message.answer(f"Добро пожаловать в панель администратора!🤗\n\n👤пользователи: {users_count}\n👥группы: {groups_count}\n\n👇 Выбирайте меню", reply_markup=admin_main_btn())

@dp.callback_query_handler(text="export_votes")
async def export_votes(call: types.CallbackQuery):
    await call.message.answer_chat_action("upload_document")
    # Excel faylni yaratish
    file_name = await export_votes_to_excel()

    # Faylni foydalanuvchiga yuborish
    if file_name:
        with open(file_name, 'rb') as file:
            await call.message.reply_document(file)
 
@dp.callback_query_handler(text='send_message_forward')
async def SendMessageForward(call: types.CallbackQuery):
    print("keldi")
    await StateSendForward.getMsg.set()
    await call.message.delete()
    await call.message.answer("Напиши мне сообщение, Я перешлю(forward) сообщение всем пользователям.")
    
@dp.message_handler(content_types=types.ContentTypes.ANY, state=StateSendForward.getMsg)
async def SendForward_bot(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.reply("Отправка...")
    users = await db.select_all_users()
    if users == False: 
        await msg.answer("Пользователи не существует")
        return
    
    sended=0
    no_sended=0
    
    for user in users:
        try:
            user_id = user['telegram_id']
            await msg.forward(user_id)
            await asyncio.sleep(.07)
            sended +=1
        except:
            no_sended +=1
            continue
    await msg.reply(f"отправлено: {sended}\nне был отправлен: {no_sended}")


@dp.callback_query_handler(text='send_message')
async def SendMessage(call: types.CallbackQuery):
    await StateSendMessage.getMsg.set()
    await call.message.delete()
    await call.message.answer("Напиши мне сообщение, Я перешлю сообщение всем пользователям.")
    
@dp.message_handler(content_types=types.ContentTypes.ANY, state=StateSendMessage.getMsg)
async def SendMessage_bot(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.reply("Отправка...")
    users = await db.select_all_users()
    if users == False: 
        await msg.answer("Пользователи не существует")
        return
    
    sended=0
    no_sended=0
    
    kb = msg.reply_markup
    for user in users:
        try:
            user_id = user['telegram_id']
            await msg.copy_to(user_id, reply_markup=kb)
            await asyncio.sleep(.07)
            sended +=1
        except:
            no_sended +=1
            continue
    await msg.reply(f"отправлено: {sended}\nне был отправлен: {no_sended}")

@dp.callback_query_handler(text='add_channel')
async def SendMessageForward(call: types.CallbackQuery):
    await ChannelState.set_channel_id.set()
    await call.message.delete()
    await call.message.answer("Отправьте мне channel_id канала")

@dp.message_handler(state=ChannelState.set_channel_id, content_types=types.ContentTypes.TEXT)
async def add_channel(message: types.Message, state: FSMContext):
    try:
        channel_id = message.text   
        await message.bot.get_chat(channel_id)
        await db.add_channel(channel_id)
        await state.finish()
        await message.answer("Канал добавлен ✅")
    except Exception as e:
        print(e)
        await message.answer("Ошибка")
    
@dp.callback_query_handler(text='delete_channel')
async def delete_channel(call: types.CallbackQuery):
    channels = await db.select_all_channels(limit=50, offset=0)
    if len(channels) == 0:
        await call.message.answer("Каналы не существуют")
        return
    data = []
    for x in channels:
        get_channel = await bot.get_chat(x[1])
        data.append(types.InlineKeyboardButton(text=get_channel.title, url=get_channel.invite_link))
        data.append(types.InlineKeyboardButton(text="❌", callback_data=f"delete_channel_{x[1]}"))
    kb = types.InlineKeyboardMarkup(row_width=2)
    await call.message.reply("Выберите канал для удаления", reply_markup=kb.add(*data))

@dp.callback_query_handler(text_contains='delete_channel')
async def delete_channel(call: types.CallbackQuery):
    channel_id = call.data.split("_")[-1]
    await db.delete_channel(channel_id)
    await call.answer("Канал удален ✅")
    channels = await db.select_all_channels(limit=50, offset=0)
    data = []
    for x in channels:
        get_channel = await bot.get_chat(x[1])
        data.append(types.InlineKeyboardButton(text=get_channel.title, url=get_channel.invite_link))
        data.append(types.InlineKeyboardButton(text="❌", callback_data=f"delete_channel_{x[1]}"))
    kb = types.InlineKeyboardMarkup(row_width=2)
    await call.message.edit_text("Выберите канал для удаления", reply_markup=kb.add(*data))