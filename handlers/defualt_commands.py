from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message

from db import Db_bot
from keyboards.defualt_keyboard import get_start_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет!👋")
    await message.answer(
        "Я твой дневник настроения, буду записывать каждый день твоё самочувствие,настроение и короткий комментарий к дню.✍️\n"+
        "Вечерами я буду напоминать тебе о прохождение ежедневной проверки настроения.📩\n"+
        "Чтобы начать нажми на кнопку!👇",
        reply_markup=get_start_keyboard()
    )

@router.message(Command("month"))
async def cmd_moodMonth(message:Message, db: Db_bot):
    feelings = await db.get_checkup_date(message.from_user.id)
    content = ""
    for table in feelings:
        content = "".join([content,
                    f"🗓Дата чекапа:{table[3]}\n" +
                    f"Самочувствие:{table[0]}\n" +
                    f"Настроение: {table[1]}\n" +
                    f"Комментирий к дню:{table[2]}\n"])      
    await message.answer(
        f"Список пройденных чекапов за текущий месяц:\n" +
        f"{content}",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(Command("profile"))
async def cmd_profile(message: Message, db: Db_bot):
    if(await db.user_exists(message.from_user.id)):
        user = await db.get_user(message.from_user.id)
        await message.answer(
            f"Твоё id:{user[0]}\n" +
            f"Возраст:{user[1]}\n" +
            f"Имя:{user[2]}\n" +
            f"Гендер:{user[3]}"
        )
    else:
        await message.answer("Я тебя не знаю!")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Команды:\n"+
                        "/profile: выводит информацию о тебе\n" +
                        "/month: выводит все записи пройденных чекапов за текущий месяц")