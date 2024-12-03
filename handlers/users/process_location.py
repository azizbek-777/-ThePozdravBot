from datetime import datetime
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
import pytz
from timezonefinder import TimezoneFinder

from lang.messages import MESSAGES
from loader import dp
from utils.misc import add_group_message

@dp.message_handler(content_types=["location"])
async def process_location(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    
    if timezone_str:
        timezone = pytz.timezone(timezone_str)
        current_time = datetime.now(timezone)
        utc_offset = current_time.utcoffset().total_seconds() / 3600
        gmt_offset = f"GMT{'+' if utc_offset >= 0 else ''}{int(utc_offset)}"

        await message.answer(
            MESSAGES[locale]["birthday_saved_timezone"].format(gmt_offset),
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await add_group_message(message, dp, locale)