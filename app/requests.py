from sqlalchemy import select

from .models import async_session
from .models import Message

async def db_set_message(message_text : str, username : str, message_attachment : str,
                        user_id : int, message_id : int) -> None:
    '''Set message in the database'''
    async with async_session() as session:
        session.add(Message(username = username,
                            message = message_text,
                            attachment = message_attachment,
                            user_id = user_id,
                            message_id = message_id))
        await session.commit()


async def db_delete_data(data_id : int) -> None:
    '''Deletes data by data id through scalars'''
    async with async_session() as session:
        message = await session.execute(select(Message).where(Message.id == data_id))
        result = message.scalars().first()
        await session.delete(result)
        await session.commit()



#Honestly, the way I get data here is just sucks.
#I think there're more optimized ways without a need to acess db multiple times 1.7.2023
#I reconsidering the way, how bot will read messages. It's rather peak of comedy than a function.
async def db_read_message():
    '''Tries to read message from 
    database, transform it into the list.
    Returns the cortege consist of:

    0. message id in db
    1. username, returns None if there's no such
    2. text within the message 
    3. attachment id
    4. telegram id of the user
    5. id of the message in chat
    '''
    async with async_session() as session:
        try:
            q = select(Message.id,
               Message.username,
               Message.message,
               Message.attachment,
               Message.user_id,
               Message.message_id
               ).order_by(Message.id.asc()).limit(1)
            res_str = await session.execute(q)
            data = res_str.fetchall()[0]
           
            await db_delete_data(data_id = data[0])

        except IndexError:
            data = None

    return data