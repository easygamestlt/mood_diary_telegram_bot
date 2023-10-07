from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states import RegistrationState

from db import Db_bot
router = Router()


@router.callback_query(F.data == "registration")
async def start_registration(
    callback: types.CallbackQuery,
    state: FSMContext,
    db = Db_bot        
):
    if(not await db.user_exists(callback.from_user.id)):
        await callback.message.answer(
            text="Как к тебе обращаться?"
        )
        await state.set_state(RegistrationState.reg_name)
    else:
        await callback.message.answer(
            text="Тебя я уже знаю, тебе не нужно регистрироваться"
        )