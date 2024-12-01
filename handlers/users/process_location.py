from datetime import datetime
from aiogram.types import Message, ReplyKeyboardRemove
import pytz
from timezonefinder import TimezoneFinder


from loader import dp
from utils.misc import add_group_message

@dp.message_handler(content_types=["location"])
async def process_location(message: Message):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    # Vaqt zonasi aniqlash
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    
    if timezone_str:
        # Vaqt mintaqasini aniqlash
        timezone = pytz.timezone(timezone_str)
        current_time = datetime.now(timezone)
        utc_offset = current_time.utcoffset().total_seconds() / 3600
        gmt_offset = f"GMT{'+' if utc_offset >= 0 else ''}{int(utc_offset)}"

        # Foydalanuvchiga xabar yuborish
        await message.answer(
            f"🎉 Спасибо! Ваш день рождения сохранен, "
            f"и ваша таймзона установлена ({gmt_offset}). "
            f"Теперь я буду напоминать о вашем дне рождения в нужное время.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await add_group_message(message, dp)