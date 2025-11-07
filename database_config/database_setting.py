from os import getenv
from dotenv import load_dotenv
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

engine = create_async_engine(url=DATABASE_URL) #type: ignore
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
        # await conn.run_sync(Base.metadata.drop_all)
        # print('База удалена')
        await conn.run_sync(Base.metadata.create_all)
        print('База создана')
