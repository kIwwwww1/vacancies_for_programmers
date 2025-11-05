import asyncio
from aiogram import Dispatcher, Bot
from os import getenv
from dotenv import load_dotenv
from database_config.database_setting import create_database
from logging import basicConfig, INFO 
from commands.main_commands import user_router

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN) # type: ignore
dp = Dispatcher()

async def main():
    await create_database()
    print(' Бот запущен '.center(80, '='))
    print(basicConfig(level=INFO))
    dp.include_router(user_router)
    await dp.start_polling(bot)
    print(' Бот остановлен '.center(80, '='))

if __name__ == '__main__':
    asyncio.run(main())


