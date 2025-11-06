from os import getenv
from dotenv import load_dotenv
from sqlalchemy import select
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from database_config.database_setting import User, create_session
from user_keyboards.reply_kb import create_note

load_dotenv()

CHAT_ID = int(getenv('CHAT_ID')) # type: ignore

user_router = Router()



@user_router.message(CommandStart())
async def start_command(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.username
    async with create_session() as session:
        user = (await session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
        if not user:
            session.add(User(id=user_id, user_name=name))
            await message.answer(f'Привет {name}', reply_markup=create_note)
        else:
            await message.answer(f'С возвращением, {name}!', reply_markup=create_note)


