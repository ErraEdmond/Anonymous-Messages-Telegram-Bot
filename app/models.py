from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, Integer
import aiogram, sqlite3

engine = create_async_engine(url='sqlite+aiosqlite:///database.sqlite3', echo=True)
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120))
    message: Mapped[str] = mapped_column(String(2000), nullable=True)
    attachment: Mapped[str] = mapped_column(String(2000), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
async def async_main():
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)
