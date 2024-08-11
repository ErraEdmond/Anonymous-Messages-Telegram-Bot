from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 



first_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Выберите действие', 
                                     keyboard=[
    [KeyboardButton(text='Послать сообщение анонимно ✉️'), KeyboardButton(text='Послать сообщение с подписью 📧')],
    [KeyboardButton(text='Админ панель 🔑')]
    ])

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                    input_field_placeholder='Добро пожаловать, админ!',  
                                    keyboard=[
    [KeyboardButton(text='Прочитать сообщения ✔️'), KeyboardButton(text='Отключить отправку 🔇')],
    [KeyboardButton(text='Добавить админа 🏷')]
])

go_back = ReplyKeyboardMarkup(resize_keyboard=True,
                              input_field_placeholder='Выберите действие', 
                              keyboard=[
                                  [KeyboardButton(text='Назад')]
                                  ])
