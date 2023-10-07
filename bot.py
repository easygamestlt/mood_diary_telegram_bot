import os
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import defualt_commands, callbacks, registration, checkup
from schedulers import start_daily_scheduler
from db import Db_bot

load_dotenv()

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Variable in .env file DB_URL 
    db_bot = Db_bot(os.getenv('DB_URL'))
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    dp = Dispatcher(storage=MemoryStorage(), scheduler=scheduler, db = db_bot)

    # Variable in .env file DB_URL
    bot = Bot(token=os.getenv('BOT_TOKEN'))

    # start mailing to existing users during startup/restart time
    await start_daily_scheduler(bot,scheduler,db_bot)
    # run schedulers
    scheduler.start()

    dp.include_routers(
        defualt_commands.router,
        callbacks.router,
        registration.router,
        checkup.router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())