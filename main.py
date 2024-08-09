import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import keyboard as kb

from config import TOKEN, ADMIN


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def hello(message : Message):
    await message.answer(
        '''Привет! Это анонимка канала "Игра Преколов", здесь ты можешь задать любой вопрос и получить ответ''',
        reply_markup=kb.first_keyboard)
    await asyncio.sleep(20)

@dp.message(F.text=='Админ панель 🔑')
async def get_admin_panel(message : Message):
    if str(message.from_user.id) in ADMIN:
        await message.answer(f'''Hello, Admin!
Amount of messages:''', reply_markup=kb.admin_keyboard)
    else:
        await message.answer(text='Вас нет в базе администраторов!', reply_markup=kb.go_back)
        


async def main():
    await dp.start_polling(bot) #waiting to transfuse a request from a TG server to the bot


if __name__ == '__main__': 
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot have terminated') 