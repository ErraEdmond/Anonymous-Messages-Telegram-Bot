from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

class Sending_Message(BaseMiddleware): 

    async def __cal__(self,
                  handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                  event: TelegramObject,
                  data: Dict[str, Any]) -> Any:
        return None