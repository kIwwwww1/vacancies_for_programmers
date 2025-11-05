from sqlalchemy import select
from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from os import getenv
from dotenv import load_dotenv
from database_config.database_setting import User, create_session

load_dotenv()

CHAT_ID = getenv('CHAT_ID')

user_router = Router()

@user_router.message(CommandStart())
async def start_command(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.username
    async with create_session() as session:
        user = (await session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
        if not user:
            session.add(User(id=user_id, user_name=name))
            await message.answer(f'Привет {name}')
        else:
            await message.answer(f'С возвращением, {name}!')
