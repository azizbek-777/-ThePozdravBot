from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from utils.db_api.postgresql import Database
from utils.misc import send_congratulation_message

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

scheduler = AsyncIOScheduler()

def scheduler_jobs():
    scheduler.add_job(
        send_congratulation_message,
        "interval",
        minutes=30,
        args=(dp,db),
    )