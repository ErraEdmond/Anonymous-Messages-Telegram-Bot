from aiogram.fsm.state import State, StatesGroup

class SendingMessage(StatesGroup):
    sending_anon = State()
    sending = State()