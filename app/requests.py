from app.modules_db import async_session
from app.modules_db import Message

from sqlalchemy import select, delete

async def set_message(message_text : str, tg_id : str) -> None:
    async with async_session() as session: 
        message = session.add(Message(user_id = tg_id, message = message_text))
        await session.commit()