from aiogram.types import (
                                    InlineKeyboardButton,
                                    InlineKeyboardMarkup,
                                    KeyboardButton,
                                    ReplyKeyboardMarkup,
)

first_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, 
                                    input_field_placeholder='', 
                                     keyboard=[
   [KeyboardButton(text='Послать сообщение анонимно ✉️'), KeyboardButton(text='Послать сообщение с подписью 📧')],
    [KeyboardButton(text='Админ панель 🔑')]
    ])

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                    input_field_placeholder='Добро пожаловать, админ!',  
                                    keyboard=[
    [KeyboardButton(text='Прочитать сообщения ✔️'), KeyboardButton(text='Отключить отправку 🔇')],
    [KeyboardButton(text='Добавить админа 🏷'), KeyboardButton(text='Назад')]
])

go_back = ReplyKeyboardMarkup(resize_keyboard=True,
                              input_field_placeholder='Выберите действие', 
                              keyboard=[
                                  [KeyboardButton(text='Назад')]
                                  ])

reading_messages = ReplyKeyboardMarkup(resize_keyboard=True,
                                       input_field_placeholder='Выберите опцию',
                                       keyboard=[
                                           [KeyboardButton(text='Читать сообщения'), KeyboardButton(text='Закончить чтение')],
                                           [KeyboardButton(text='Ответить')]
                                       ]
                                       )

answer_message_action = InlineKeyboardMarkup(inline_keyboard = [
[InlineKeyboardButton(text='Ban user⛔', callback_data=None), InlineKeyboardButton(text='Send appreciation')],
[InlineKeyboardButton(text='Sent an answer', callback_data=None)]
])