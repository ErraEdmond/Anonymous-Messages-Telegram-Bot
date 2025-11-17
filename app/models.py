from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String, Integer

engine = create_async_engine(url='sqlite+aiosqlite:///database.sqlite3', echo=True)
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=True)
    message: Mapped[str] = mapped_column(String(2000), nullable=True)
    attachment: Mapped[str] = mapped_column(String(2000), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)


async def async_main():
    '''Create table and starts asyncs main db cycle'''
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)
