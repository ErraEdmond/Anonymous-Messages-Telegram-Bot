from aiogram.fsm.state import State, StatesGroup

class SendingMessage(StatesGroup):
    sending = State()


class AdminState(StatesGroup):
    is_admin = State()
    reading = State()

print(AdminState)
print(AdminState.is_admin.__getstate__())


