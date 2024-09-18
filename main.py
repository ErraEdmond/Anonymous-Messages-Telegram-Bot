import asyncio

from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import rt
from modules_db import async_main

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(rt)
    await dp.start_polling(bot) 
    await async_main()
    #waiting to transfuse a request from a TG server to the bot

if __name__ == '__main__': 
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot have terminated') 