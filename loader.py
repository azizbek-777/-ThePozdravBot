from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from data import config
from utils.db_api.postgresql import Database
from utils.misc import send_congratulation_message

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

scheduler = AsyncIOScheduler()

def scheduler_jobs():
    job_id = "send_congratulation_message"

    all_jobs = scheduler.get_jobs()
    print('all_jobs', all_jobs)
    for job in all_jobs:
        if job.id != job_id: 
            scheduler.remove_job(job.id)

    scheduler.add_job(
        send_congratulation_message,
        CronTrigger(hour=0, timezone=timezone('Asia/Tashkent')),
        args=(dp, db),
        id=job_id,
        replace_existing=True
    )
    print(f"Job '{job_id}' successfully added.")

