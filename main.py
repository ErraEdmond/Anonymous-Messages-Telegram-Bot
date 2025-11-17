import asyncio
import sys 
import logging

from handlers import rt
from app.models import async_main 
from config import bot, dp


async def main():
    '''Main loop'''
    await async_main()
    dp.include_router(rt)
    await dp.start_polling(bot)
    #waiting to transfuse a request from a TG server to the bot 
    #instance is a class, containing Dispatcher and Bot itself.


if __name__ == '__main__': 
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot have terminated') 