import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv
from database_config.database_setting import create_database
from logging import basicConfig, INFO 
from commands.main_commands import user_router
from commands.create_vacancy import vacancy_router
from commands.create_resume import resume_router

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN) # type: ignore
dp = Dispatcher(storage=MemoryStorage())

async def main():
    await create_database()
    print(' Бот запущен '.center(20, '='))
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(user_router, vacancy_router, resume_router)
    await dp.start_polling(bot)
    print(' Бот остановлен '.center(20, '='))

if __name__ == '__main__':
    asyncio.run(main())


