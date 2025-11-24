from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import keyboard as kb
from fsm import SendingMessage, AdminState
from config import ADMIN, START_MESSAGE, BANNED_USERS
from app.requests import db_set_message, db_read_message
from answer_message import answer_to_user


rt = Router()

@rt.message(F.from_user.id == BANNED_USERS)
async def banned_users(message: Message):
    await message.reply('Ты был забанен, лол!')


@rt.message(F.text == 'Назад')
@rt.message(CommandStart())
async def hello(message : Message) -> None:
    await message.answer(START_MESSAGE, reply_markup=kb.first_keyboard)


@rt.message(F.text == 'Админ панель 🔑')
async def get_admin_panel(message : Message, state : FSMContext) -> None:
    if str(message.from_user.id) in ADMIN:
        await message.answer('''Hello, Admin! Amount of messages:''', 
                            reply_markup=kb.admin_keyboard)
        await state.set_state(AdminState.is_admin)
        await state.update_data(is_admin = True)
    else:
        await message.answer(text='Вас нет в базе администраторов!',
                            reply_markup=kb.go_back)


if AdminState.is_admin:
    # @rt.message(str(AdminState.reading.__getstate__) == 'False')
    @rt.message(F.text == 'Прочитать сообщения ✔️')
    async def read_messages(message : Message, state : FSMContext) -> None:
        await state.set_state(AdminState.reading)
        await state.update_data(reading = True)
        await message.answer(text='Отлично, вот сообщения:',
                            reply_markup=kb.reading_messages)

    @rt.message(F.text == 'Читать сообщения')
    async def reading_messages(message : Message, state: FSMContext):
        message_db = await db_read_message()
        
        if message_db is None:
            await message.answer(text='Новых сообщений нет!')
            return
        
        await state.set_state(AdminState.message_data)
        await state.update_data(message_data = [message_db[4], message_db[5]])

        if message_db[3] is not None:
            await message.answer_photo(caption = f'''"{message_db[2]} by {message_db[1]}"''',
                                       reply_markup = kb.answer_message_action,
                                       photo = message_db[3])
            await state.update_data(message_data=[message.from_user.get('chat').get('id')])
        else:
            await message.answer(text = f'''{message_db[2]} by {message_db[1]}''',
                                reply_markup = kb.reading_messages)
    

    @rt.message(F.text == 'Ответить' and AdminState.message_data)
    async def answer_message(message : Message, state: FSMContext):
        await message.answer(text='Напишите сообщение')
        await state.set_state(AdminState.answer_message)


    @rt.message(AdminState.answer_message)
    async def answer_message_2 (message: Message, state: FSMContext): 
        data = await state.get_data()
        data = data['message_data']
        await answer_to_user(text=f'ВАМ ОТВЕТИЛИ: "{message.text}"', chat_id=data[0], message_id=data[1])
        await message.answer(text='Сообщение отправлено!', reply_markup=kb.reading_messages)
        state.clear()
        

    @rt.message(F.text == 'Закончить чтение')
    async def end_of_reading(message : Message, state : FSMContext) -> None:
        await state.clear()
        await message.reply('Отлично почитали :)', reply_markup= kb.first_keyboard)


@rt.message(Command('info'))
async def get_message_info(message : Message) -> None:
    await message.reply(text=f'''
                    Message id: {message.message_id}, 
                    user id: {message.from_user.id}, 
                    text of message of: {message.text}
                    dump: {message.model_dump()}'''
                    )


@rt.message(F.text == 'Послать сообщение анонимно ✉️')
@rt.message(F.text == 'Послать сообщение с подписью 📧')
async def send_message_1(message : Message, state: FSMContext) -> None:
    await state.set_state(SendingMessage.sending)
    if message.text == 'Послать сообщение анонимно ✉️':
        await state.update_data(sending = 'anon')
    if message.text == 'Послать сообщение с подписью 📧':
        await state.update_data(sending = 'not_anon')

    await message.reply(text='Введите сообщения',
                        reply_markup=kb.go_back)


@rt.message(SendingMessage.sending and F.photo)
async def send_message_with_photo(message : Message, state : FSMContext) -> None:
    data = await state.get_data()
    dump = message.model_dump()
    caption = dump['caption']
    photo_id = dump['photo'][0]['file_id']
    chat_id = dump['chat']['id']
    us = str(dump['from_user']['username'])
    message_id = int(dump['message_id'])

    if us != 'None':
        us = '@' + us

    if data.get('sending') == 'not_anon':
        await db_set_message(username = us,
                             message_text = caption,
                             message_attachment = photo_id,
                             user_id = chat_id,
                             message_id = message_id
                             )

    if data.get('sending') == 'anon':
        await db_set_message(username = None,
                            message_text = caption,
                            message_attachment = photo_id, 
                            user_id = chat_id,
                            message_id = message_id
                            )

    await message.reply('Cообщение отправлено!')
    await state.clear()


@rt.message(SendingMessage.sending) 
async def send_message_2(message : Message, state : FSMContext) -> None:
    data = await state.get_data()
    dump = message.model_dump()
    text = dump['text']
    chat_id = dump['chat']['id']
    us = str(dump['from_user']['username'])
    message_id = int(dump['message_id'])
    print(us)

    if us != 'None':
        us = '@' + us


    if data.get('sending') == 'not_anon':
        await db_set_message(username = us,
                             message_text = text,
                             message_attachment = None,
                             user_id = chat_id,
                             message_id= message_id
                             )
    if data.get('sending') == 'anon':   
        await db_set_message(username = None,
                            message_text = text,
                            message_attachment = None,
                            user_id = chat_id,
                            message_id = message_id
                            )

    await message.reply('Cообщение отправлено!')
    await state.clear()


# message_message_attachment=message.photo[-1].file_id
@rt.callback_query(F.data == 'appreciation')
async def send_appreciation(): 
    pass


@rt.message(Command('chat_id', 'Chat_id'))
async def get_chat_id(message : Message) -> None: 
    chat_id = message.model_dump().get('chat').get('id')
    chat_info = await message.bot.get_chat(chat_id=chat_id)
    await message.reply(text=f'{chat_info}, {type(chat_info)}')


@rt.message(Command('user_id'))
async def get_id(message : Message) -> None: 
    user_id = message.model_dump()
    await message.reply(
        text=f"ur id is: {user_id}") 