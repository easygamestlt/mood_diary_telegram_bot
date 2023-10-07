from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import Db_bot
from keyboards.checkup_keyboard import get_start_checkup_kb

"""Отправляем сообщение пользователю с предложением пройти чекап"""      
async def send_daily_message(bot: Bot, user_id:int):
    await bot.send_message(
        chat_id=user_id,
        text="Напоминание о том, чтобы пройти чекап",
        reply_markup=get_start_checkup_kb()
    )

"""Функция запуска рассылки, запускаемая каждый день в 19 часов вечера"""
async def start_daily_scheduler(bot:Bot, scheduler:AsyncIOScheduler, db_bot:Db_bot):
    #Получаем всех зарегистрированных пользователей
    users = await db_bot.get_users()

    for user in users:
        for id in user:
            scheduler.add_job(send_daily_message, trigger='cron', hour=19,
                        kwargs=({'bot':bot, 'user_id': id}))