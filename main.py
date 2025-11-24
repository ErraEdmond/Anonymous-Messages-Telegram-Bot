import asyncio
import sys
import logging

from handlers import rt
from app.models import async_main
from config import TOKEN
from answer_message import inst

async def main():
    '''Main loop'''
    inst.bot_ini(token=TOKEN)
    await async_main()
    inst.dp.include_router(rt)
    await inst.dp.start_polling(inst.bot)
    #waiting to transfuse a request from a TG server to the bot 
    #instance is a class, containing Dispatcher and Bot itself.


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot have terminated') 