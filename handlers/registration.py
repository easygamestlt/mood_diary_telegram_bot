from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from schedulers import send_daily_message

from states import RegistrationState
from keyboards.defualt_keyboard import get_gender_kb

from db import Db_bot

router = Router()

@router.message(RegistrationState.reg_name)
async def get_gender(message: Message, state: FSMContext):
    await state.update_data(reg_name=f"{message.text}")
    await message.answer(
        text=f"Хорошо {message.text}, теперь узнаем твой пол.\n"+
        "Выбери кнопку снизу с твоим гендером",
        reply_markup=get_gender_kb()
    )
    await state.set_state(RegistrationState.reg_gender)

@router.message(RegistrationState.reg_gender)
async def get_age(message:Message, state: FSMContext):
    await state.update_data(reg_gender=f"{message.text}")
    await message.answer(
        text="Отлично, осталось совсем чуть-чуть, укажи свой возраст",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationState.reg_age)

@router.message(RegistrationState.reg_age)
async def registration_user(message:Message, state:FSMContext, db:Db_bot, scheduler:AsyncIOScheduler):
    user_data = await state.get_data()
    try:
        await db.add_user(user_id=message.from_user.id, age=int(message.text), name=user_data['reg_name'],gender=user_data['reg_gender'])
        await message.answer(
        text=f"Твои данные записались"
        )
    except:
        print("Error, данные не записались")
        await message.answer(
            text="Не получилось записать твои данные, нажми заново на кнопку начать, чтобы попробовать снова"
        )

    await message.answer(
        text=f"Твои данные:\n"+
            f"Имя:{user_data['reg_name']}\n"+
            f"Пол:{user_data['reg_gender']}\n"+
            f"Возраст:{message.text}"
    )
    scheduler.add_job(send_daily_message, trigger='cron', hour=19,
                    kwargs=({'bot':message.bot, 'user_id': message.from_user.id}))
    await state.clear()