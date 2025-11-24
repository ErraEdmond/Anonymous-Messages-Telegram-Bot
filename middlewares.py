from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class BannedUsers(BaseMiddleware): 
    async def __cal__(self,
                  handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                  event: TelegramObject,
                  data: Dict[str, Any]) -> Any:
        pass 



    