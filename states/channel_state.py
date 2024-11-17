from aiogram.dispatcher.filters.state import State, StatesGroup

class ChannelState(StatesGroup):
    set_channel_id = State()