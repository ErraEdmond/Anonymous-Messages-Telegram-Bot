from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class BannedUsers(BaseMiddleware): 
    async def __cal__(self,
                  handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                  event: TelegramObject,
                  data: dict[str, Any]) -> Any:
        pass 



    