import asyncio
from aiogram import Dispatcher, Bot
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
CHAT_TOKEN = getenv('CHAT_TOKEN')

bot = Bot(token=BOT_TOKEN) # type: ignore
dp = Dispatcher()

async def main():
    # await dp.include_router()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


