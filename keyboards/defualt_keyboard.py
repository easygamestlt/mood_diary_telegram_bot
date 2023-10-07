from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from cbdata import GenderCallbackFactory

def get_start_keyboard() -> InlineKeyboardMarkup:
    builder  = InlineKeyboardBuilder()
    builder.button(
        text="Начать", callback_data="registration"
    )
    return builder.as_markup(resize_keyboard=True)

def get_gender_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="М", callback_data=GenderCallbackFactory(gender="male")
    )
    builder.button(
        text="Ж", callback_data=GenderCallbackFactory(gender="female")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)