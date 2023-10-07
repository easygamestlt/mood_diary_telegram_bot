from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from states import CheckupState
from db import Db_bot
from keyboards.checkup_keyboard import get_feeling_kb


router = Router()

@router.message(F.text == "Пройти чекап")
async def check_feel(message:Message, state: FSMContext, db: Db_bot):
    if((await db.user_exists(message.from_user.id)) and (not await db.checkup_date_exists(message.from_user.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))):
        await message.answer(
            text="Давай проверим твоё состояние на сегодня! Как твоё самочувствие?",
            reply_markup=get_feeling_kb()
        )
        await state.set_state(CheckupState.check_feel)
    elif(await db.checkup_date_exists(message.from_user.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))):
        await message.answer(
            text="Ты сегодня уже проходил чекап"
        )
    elif (not await db.user_exists(message.from_user.id)):
        await message.answer(
            text="Тебя я не знаю, чтобы пройти чекап, мне надо тебя узнать, пожалуйста, пройди регистрацию"
        )

@router.message(CheckupState.check_feel)
async def check_mood(message:Message, state: FSMContext):
    await state.update_data(chk_feel=f"{message.text}")
    await message.answer(
            text="Теперь давай узнаем, какое сегодня твоё настроение.",
            reply_markup=get_feeling_kb()
        )
    await state.set_state(CheckupState.check_mood)

@router.message(CheckupState.check_mood)
async def check_comment(message:Message, state: FSMContext):
    await state.update_data(chk_mood=f"{message.text}")
    await message.answer(
            text="Оставь свой комментарий к сегодняшнему дню",
            reply_markup=types.ReplyKeyboardRemove()
        )
    await state.set_state(CheckupState.check_comment)

@router.message(CheckupState.check_comment)
async def checkup_user(message:Message, state: FSMContext, db: Db_bot):
    user_data = await state.get_data()
    now = datetime.now()
    await message.answer(
        text='Данные на запись:\n' +
        f'Самочувствие:{user_data["chk_feel"]}\n'+
        f'Настроение:{user_data["chk_mood"]}\n'+
        f'Комментарий:{message.text}\n'+
        f'Дата:{now.strftime("%Y-%m-%d %H:%M:%S")}'
    )
    try:
        await db.add_checkup(
            user_id=message.from_user.id, 
            feel=user_data["chk_feel"],
            mood=user_data["chk_mood"],
            comment=message.text,
            date=now.strftime('%Y-%m-%d %H:%M:%S')
        )
    except:
        await message.answer(
            text="Не получается записать данные"
        )
    await state.clear()