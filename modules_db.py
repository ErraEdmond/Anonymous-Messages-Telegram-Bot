from sqlalchemy.orm import Relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String

engine = create_async_engine(url='sqlite+aiosqlite:///sqlite3.db')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(20))
    tg_id = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)