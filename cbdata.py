from aiogram.filters.callback_data import CallbackData

class GenderCallbackFactory(CallbackData, prefix = "gender"):
    gender: str