import asyncio
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager

engine = create_async_engine('postgresql+asyncpg://postgres:12345@localhost:5432/postgres')
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    user_name: Mapped[str] = mapped_column(nullable=False)

@asynccontextmanager
async def create_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print('База удалена')
        await conn.run_sync(Base.metadata.create_all)
        print('База создана')
