from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import keyboard as kb
from fsm import SendingMessage, AdminState
from config import ADMIN


rt = Router()


@rt.message(F.text == 'Назад')
@rt.message(CommandStart())
async def hello(message : Message) -> None:
    await message.answer(
        '''Привет! Это анонимка канала "Игра Преколов", здесь ты можешь задать любой вопрос и получить ответ''',
        reply_markup=kb.first_keyboard)


@rt.message(F.text == 'Админ панель 🔑')
async def get_admin_panel(message : Message, state : FSMContext) -> None:
    if str(message.from_user.id) in ADMIN:
        await message.answer(f'''Hello, Admin! Amount of messages:''', reply_markup=kb.admin_keyboard)
        await state.set_state(AdminState.is_admin)
        await state.update_data(is_admin = True)
    else:
        await message.answer(text='Вас нет в базе администраторов!', reply_markup=kb.go_back)


if AdminState.is_admin:
    # @rt.message(str(AdminState.reading.__getstate__) == 'False')
    @rt.message(F.text == 'Прочитать сообщения ✔️')
    async def read_messages(message : Message, state : FSMContext) -> None:
        await state.set_state(AdminState.reading)
        await state.update_data(reading = True)
        print(AdminState.reading.__getstate__)
        await message.answer(text='Отлично, вот сообщения:', reply_markup=kb.reading_messages)
    
    @rt.message(F.text == 'Читать сообщения')
    async def reading_messages(message : Message):
        with open(file='messages.txt', mode='r+') as f:
            new_message = f.readline(20)
        await message.answer(text=new_message, reply_markup=kb.reading_messages)
    
    @rt.message(F.text == 'Закончить чтение')
    async def end_of_reading(message : Message, state : FSMContext) -> None: 
        await state.update_data(reading = False)


@rt.message(Command('info'))
async def get_message_info(message : Message) -> None:
    await message.reply(text=f'''
                    Message id: {message.message_id}, 
                    user id: {message.from_user.id}, 
                    text of message of: {message.text}'''
                    )
    

@rt.message(F.text == 'Послать сообщение анонимно ✉️')
@rt.message(F.text == 'Послать сообщение с подписью 📧')
async def send_message_1(message : Message, state: FSMContext) -> None:
    await state.set_state(SendingMessage.sending)
    if message.text == 'Послать сообщение анонимно ✉️':
        await state.update_data(sending = 'anon')
    if message.text == 'Послать сообщение с подписью 📧':
        await state.update_data(sending = 'not_anon')
    await message.reply(text='Введите сообщения', reply_markup=kb.go_back)


@rt.message(SendingMessage.sending)
async def send_message_2(message : Message, state : FSMContext) -> None:
    data = await state.get_data()

    with open(file='messages.txt', mode='a') as f:
            if data['sending'] == 'not_anon':
                f.write(f'{message.from_user.id}, {message.text} \n')
            if data['sending'] == 'anon':
                f.write(f'Anon, {message.text} \n')
    await message.reply('Cообщение отправлено!')
    await state.clear()





