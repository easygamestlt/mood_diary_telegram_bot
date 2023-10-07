from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def get_start_checkup_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="Пройти чекап"
    )
    return builder.as_markup(resize_keyboard=True)

def get_feeling_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="Отличное"
    )
    builder.button(
        text="Хорошое"
    )
    builder.button(
        text="Нормальное"
    )
    builder.button(
        text="Плохое"
    )
    builder.button(
        text="Ужасное"
    )
    builder.adjust(5)
    return builder.as_markup(resize_keyboard=True)