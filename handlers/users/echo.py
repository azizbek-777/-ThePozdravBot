from aiogram import types

from loader import dp, db
from utils.misc import subscription

# Echo bot
@dp.message_handler(state=None)
async def bot_channels_joined_user(message: types.Message):
    channels = await db.select_all_channels()
    not_joined_channels = []
    if channels == True:
        for channel in channels:
            try:
                is_joined_check = await subscription.check(user_id=message.from_user.id, channel=channel[1])
                if is_joined_check == False:
                    not_joined_channels.append(channel[1])
            except:
                continue
    
  