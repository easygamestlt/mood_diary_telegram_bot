from aiogram.fsm.state import StatesGroup,State

class RegistrationState(StatesGroup):
    reg_name = State()
    reg_gender = State()
    reg_age = State()

class CheckupState(StatesGroup):
    check_feel = State()
    check_mood = State()
    check_comment = State()
