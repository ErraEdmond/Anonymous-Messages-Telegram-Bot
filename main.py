import asyncio
import sys 
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import rt
from app.modules_db import async_main

async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(rt)
    await dp.start_polling(bot)
    #waiting to transfuse a request from a TG server to the bot 
    

if __name__ == '__main__': 
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot have terminated') 