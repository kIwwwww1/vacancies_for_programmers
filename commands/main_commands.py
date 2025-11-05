from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from os import getenv
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = getenv('CHAT_ID')

user_router = Router()

@user_router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    await message.answer('Привет')
