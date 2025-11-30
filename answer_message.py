import asyncio

from aiogram import Bot, Dispatcher

class BotConfig():
    '''Bot config class, which is must be initialized only in a main.py, by the bot_ini.'''

    def __init__(self):
        self.bot = None
        self.dp = None

    def bot_ini(self, token):
        '''Point of initialization for a bot in main.py'''
        self.bot = Bot(token=token)
        self.dp = Dispatcher()


inst = BotConfig()

async def answer_to_user(chat_id: str, text: str, message_id: int) -> None:
    '''Answer to specific message in specific chat, via bot instance'''
    await inst.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=message_id)
