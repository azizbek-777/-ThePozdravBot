import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.exceptions import ChatNotFound
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.inline import subscription_btn, nominations_btn
from keyboards.default import contact_btn
from utils.misc import subscription
from aiogram.dispatcher import FSMContext
from datetime import datetime


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    # Foydalanuvchini qo'shish yoki mavjud foydalanuvchini olish
    await add_or_notify_user(user_id, full_name, username)

    # A'zo bo'lmagan kanallarni tekshirish
    not_joined_channels = await check_user_channels(user_id)

    if not_joined_channels:
        # Agar hali a'zo bo'lmagan kanallar mavjud bo'lsa, xabar yuborish
        await message.answer(
            "Dawıs beriw ushın tómendegi kanalǵa aǵza bolıń 👇",
            reply_markup=subscription_btn(not_joined_channels)
        )
        return
    
    # Foydalanuvchining telefon raqami mavjudligini tekshirish
    if not await db.is_exists_phone_by_telegram_id(user_id):
        await message.answer("Telefon nomeringizdi jiberiń 👇", reply_markup=contact_btn)
        return
    
    # Kerakli formatga o'girib olamiz
    nominations = await db.select_all_nominations()
    data = []
    for nomination in nominations:
        name = nomination['title']  # title maydoni o'rniga to'g'ri maydon nomini kiriting
        nomination_id = nomination['id']  # id maydoni o'rniga to'g'ri maydon nomini kiriting
        data.append((name, nomination_id))

    # To'g'ri parametrni uzatish
    await message.answer("Dawıs beriw ushın tómendegi nominacialardan birin tańlań👇", reply_markup=nominations_btn(data))

@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    # A'zo bo'lmagan kanallarni tekshirish
    not_joined_channels = await check_user_channels(user_id)

    if not_joined_channels:
        await call.answer('Ele barlıq kanallarga agza bolmagansız!')
        await call.message.edit_text(
            "Dawıs beriw ushın tómendegi kanalǵa aǵza bolıń 👇",
            reply_markup=subscription_btn(not_joined_channels)
        )
    else:
        await call.message.delete()
        # Foydalanuvchining telefon raqami mavjudligini tekshirish
        if not await db.is_exists_phone_by_telegram_id(user_id):
            await call.message.answer("Telefon nomeringizdi jiberiń 👇", reply_markup=contact_btn)
        else:
            # ReplyKeyboard ni olib tashlash
            remove_keyboard = types.ReplyKeyboardRemove()
            await call.message.answer('✅', reply_markup=remove_keyboard)
            
            # 'data' ro'yxatini to'ldirish
            nominations = await db.select_all_nominations()
            data = []
            for nomination in nominations:
                name = nomination['title']  # title maydoni o'rniga to'g'ri maydon nomini kiriting
                nomination_id = nomination['id']  # id maydoni o'rniga to'g'ri maydon nomini kiriting
                data.append((name, nomination_id))

            # To'g'ri formatlangan ma'lumot bilan 'nominations_btn' funksiyasini chaqirish
            await call.message.answer(
                "Dawıs beriw ushın tómendegi nominacialardan birin tańlań👇", 
                reply_markup=nominations_btn(data)
            )

@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def contact_handler(message: types.Message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number
    user_id_by_contact = message.contact.user_id

    # Telefon raqami mavjudligini tekshirish
    if not await db.is_exists_phone_by_telegram_id(user_id):
        if user_id != user_id_by_contact:
            await message.reply("Ózińizdin telefon kontaktinizdi jiberiń!")
            return
        
        # Uzbekistan telefon raqamini tekshirish (+998 yoki 998 bilan boshlanishi kerak)
        if not (phone_number.startswith("+998") or phone_number.startswith("998")):
            await message.reply("Tek ǵana Ózbekstan telefon nomerleri qabıl etiledi!")
            return
        
        # Telefon raqamini saqlash
        await db.add_phone_by_telegram_id(user_id, phone_number)
        await message.delete()

        # ReplyKeyboard ni olib tashlash
        remove_keyboard = types.ReplyKeyboardRemove()
        await message.answer('✅', reply_markup=remove_keyboard)
        
        # Kerakli formatga o'girib olamiz
        nominations = await db.select_all_nominations()
        data = []
        for nomination in nominations:
            name = nomination['title']  # title maydoni o'rniga to'g'ri maydon nomini kiriting
            nomination_id = nomination['id']  # id maydoni o'rniga to'g'ri maydon nomini kiriting
            data.append((name, nomination_id))
            
        await message.answer("Dawıs beriw ushın tómendegi nominacialardan birin tańlań👇", reply_markup=nominations_btn(data))


@dp.message_handler(commands='reyting')
async def show_ranking(message: types.Message):
    # Reytingni olish
    await message.answer_chat_action("typing")
    try:
        ranking = await db.get_nominations_ranking()
        
        if not ranking:
            await message.answer("Házir nominaciyalar boyınsha dawıs berilgenler joq.")
            return
        
        ranking_text = "📊 *Nominaciyalar boyınsha reyting:*\n\n"
        for item in ranking:
            if item['rank'] == 1:
                # Faqat birinchi o'rin uchun "🏆" belgisini qo'shish
                ranking_text += (f"🏆 *{item['rank']}*: *{item['title']}*\n"
                                 f"  - Dawıslar sanı: {item['vote_count']}\n"
                                 f"  - Sońģı dawıs berilgen: {item['last_vote_time']}\n\n")
            else:
                ranking_text += (f"🏅*{item['rank']}*: *{item['title']}*\n"
                                 f"  - Dawıslar sanı: {item['vote_count']}\n"
                                 f"  - Sońģı dawıs berilgen: {item['last_vote_time']}\n\n")

        # Javobni yuborish
        await message.reply(ranking_text, parse_mode='Markdown')
    
    except Exception as e:
        await message.answer("Reytingni chiqarishda xatolik yuz berdi.")
        print(f"Xatolik: {e}")

@dp.callback_query_handler(text='reyting')
async def show_ranking(call: types.CallbackQuery):
    try:
        await call.message.answer_chat_action("typing")
        ranking = await db.get_nominations_ranking()
        
        if not ranking:
            await call.message.answer("Házir nominaciyalar boyınsha dawıs berilgenler joq.")
            return
        
        ranking_text = "📊 *Nominaciyalar boyınsha reyting:*\n\n"
        for item in ranking:
            if item['rank'] == 1:
                # Faqat birinchi o'rin uchun "🏆" belgisini qo'shish
                ranking_text += (f"🏆*{item['rank']}*: *{item['title']}*\n"
                                 f"  - Dawıslar sanı: {item['vote_count']}\n"
                                 f"  - Sońģı dawıs berilgen: {item['last_vote_time']}\n\n")
            else:
                ranking_text += (f"🏅*{item['rank']}*: *{item['title']}*\n"
                                 f"  - Dawıslar sanı: {item['vote_count']}\n"
                                 f"  - Sońģı dawıs berilgen: {item['last_vote_time']}\n\n")

        # Javobni yuborish
        await call.message.reply(ranking_text, parse_mode='Markdown')
    
    except Exception as e:
        await call.message.answer("Reytingni chiqarishda xatolik yuz berdi.")
        print(f"Xatolik: {e}")


@dp.callback_query_handler(text_contains='nomination:')
async def delete_channel(call: types.CallbackQuery):
    nomination_id = int(call.data.split(":")[-1])
    nomination = await db.nominate_by_id(nomination_id)
    user = await db.select_user(telegram_id=call.from_user.id)
    title = nomination['title']

    # Dastlab count_votes ni aniqlash
    count_votes = await db.count_votes(nomination_id)
    
    # Nominatsiyaning reytingini oldindan olish
    get_nomination_rank = await db.get_nomination_rank(nomination['id'])
    
    try:
        if await db.add_vote(user_id=user['id'], nomination_id=nomination['id']):
            count_votes = await db.count_votes(nomination_id)
            get_nomination_rank = await db.get_nomination_rank(nomination['id'])
            await call.answer(
                f'Siz "{title}" nominaciyasına dawıs berdińiz✅\ndawıslar sanı: {count_votes}\nreyting: {get_nomination_rank}',
                show_alert=True
            )
            return
        
        await call.answer(
            f'"{title}" nominaciyasına dawıs bergenler sanı: {count_votes}\nreyting: {get_nomination_rank}',
            show_alert=True
        )
    except asyncpg.exceptions.UniqueViolationError:
        count_votes = await db.count_votes(nomination_id)
        get_nomination_rank = await db.get_nomination_rank(nomination['id'])
        await call.answer(
            f'"{title}" nominaciyasına dawıs bergenler sanı: {count_votes}\nreyting: {get_nomination_rank}',
            show_alert=True
        )
        
async def add_or_notify_user(user_id, full_name, username):
    """Foydalanuvchini qo'shish yoki adminni xabardor qilish."""
    try:
        # Foydalanuvchini qo'shish
        user = await db.add_user(telegram_id=user_id, full_name=full_name, username=username)
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"[{full_name}](tg://user?id={user_id}) bazaģa qosıldı.\nBazada {count} paydalanıwshı bar."
        await bot.send_message(chat_id=ADMINS[0], text=msg, parse_mode="markdown")
    except asyncpg.exceptions.UniqueViolationError:
        pass


async def check_user_channels(user_id):
    """Foydalanuvchining barcha kanallarga a'zo bo'lganligini tekshirish."""
    channels = await db.select_all_channels()
    not_joined_channels = []

    for channel in channels:
        channel_id = channel[1]
        try:
            # Foydalanuvchi kanalda a'zo bo'lganmi?
            is_joined = await subscription.check(user_id=user_id, channel=channel_id)
            if not is_joined:
                get_channel = await bot.get_chat(channel_id)
                not_joined_channels.append((get_channel.title, get_channel.invite_link))
        except ChatNotFound:
            continue

    return not_joined_channels
