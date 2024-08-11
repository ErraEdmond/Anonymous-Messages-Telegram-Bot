import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import keyboard as kb
from aiogram.fsm.context import FSMContext

from config import TOKEN, ADMIN
from fsm import SendingMessage

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == 'Назад')
@dp.message(CommandStart())
async def hello(message : Message) -> None:
    await message.answer(
        '''Привет! Это анонимка канала "Игра Преколов", здесь ты можешь задать любой вопрос и получить ответ''',
        reply_markup=kb.first_keyboard)


@dp.message(F.text == 'Админ панель 🔑')
async def get_admin_panel(message : Message) -> None:
    if str(message.from_user.id) in ADMIN:
        await message.answer(f'''Hello, Admin!
Amount of messages:''', reply_markup=kb.admin_keyboard)
    else:
        await message.answer(text='Вас нет в базе администраторов!', reply_markup=kb.go_back)


@dp.message(Command('info'))
async def get_message_info(message : Message) -> None:
    await message.reply(text=f'''
                    Message id: {message.message_id}, 
                    user id: {message.from_user.id}, 
                    text of message of: {message.text}'''
                    )

@dp.message(F.text == 'Послать сообщение с подписью 📧')
async def send_message_1(message : Message, state: FSMContext) -> None:
    await state.set_state(SendingMessage.sending)
    await message.reply(text='Введите сообщения', reply_markup=kb.go_back)


@dp.message(SendingMessage.sending)
async def send_message_2(message : Message, state : FSMContext) -> None:
    with open(file='messages.txt', mode='a') as f:
         f.write(f'{message.from_user.id},{message.text}')
    await message.reply('Cообщение отправлено!')
    await state.clear()


@dp.message(F.text == 'Послать сообщение анонимно ✉️')
async def send_anon_message_1(message : Message, state: FSMContext) -> None:
    await state.set_state(SendingMessage.sending_anon)
    await message.reply(text='Введите сообщения', reply_markup=kb.go_back)

@dp.message(SendingMessage.sending_anon)
async def send_anon_message_2(message : Message, state : FSMContext) -> None:
    with open(file='messages', mode='a') as f:
        f.write(f'{message.from_user.id},{message.text}')        
    await message.reply('Сообщение отправлено!')
    await state.clear()

         

async def main():
    await dp.start_polling(bot) #waiting to transfuse a request from a TG server to the bot


if __name__ == '__main__': 
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot have terminated') 