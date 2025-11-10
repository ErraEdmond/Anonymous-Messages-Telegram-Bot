from .models import async_session
from .models import Message
import asyncio
from random import randint

from sqlalchemy import select, delete, func, Integer, table

minimal_id_function = func.min(Message.id)

async def db_set_message( message_text : str, username : str, message_attachment : str, user_id : str) -> None:
    async with async_session() as session: 
        session.add(Message(username = username, 
                            message = message_text, 
                            attachment = message_attachment, 
                            user_id = user_id))
        await session.commit()


async def db_delete_data(id : int) -> None: 
    async with async_session() as session:
        message = await session.execute(select(Message).where(Message.id == id)) 
        result = message.scalars().first()
        await session.delete(result)
        await session.commit()


#Honestly, the way I get data here is just sucks. I think there're more optimized ways without a need to acess db multiple times 1.7.2023
#I reconsidering the way, how bot will read messages. It's rather peak of comedy than a function.
async def db_read_message() -> None:
    async with async_session() as session:
        try:
            try:
                anon = randint(0,1)
                if anon: 
                    q = select(Message.id, Message.message, Message.user_id, Message.attachment).where(Message.user_id == 'Anon').group_by(Message.id).having(Message.id == func.min(Message.id))
                else:
                    q = select(Message.id, Message.message, Message.user_id, Message.attachment).where(Message.user_id != 'Anon').group_by(Message.id).having(Message.id == func.min(Message.id))
               
                res_str = await session.execute(q)
                message = list(res_str)[0]
                message_id,  message_text, message_us, photo_id = list(message)[0], list(message)[1], list(message)[2], list(message)[3]
                finale_message = f'''"{message_text}" by {message_us}'''

                await db_delete_data(id=message_id)

                
            except: 
                anon = not anon
                if anon: 
                    q = select(Message.id, Message.message, Message.user_id, Message.attachment).where(Message.user_id == 'Anon').group_by(Message.id).having(Message.id == func.min(Message.id))
                else:
                    q = select(Message.id, Message.message, Message.user_id, Message.attachment).where(Message.user_id != 'Anon').group_by(Message.id).having(Message.id == func.min(Message.id))
               
                res_str = await session.execute(q)
                message = list(res_str)[0]
                message_id,  message_text, message_us, photo_id = list(message)[0], list(message)[1], list(message)[2], list(message)[3]
                finale_message = f'''"{message_text}" by {message_us}'''    
                await db_delete_data(id=message_id)
        except: 
            finale_message = 'База данных пуста'
    return finale_message, photo_id