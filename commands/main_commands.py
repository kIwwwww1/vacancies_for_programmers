from os import getenv
from dotenv import load_dotenv
from sqlalchemy import select
from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database_config.database_setting import User, create_session
from user_keyboards.reply_kb import ReplyTextCommand, create_note

load_dotenv()

CHAT_ID = int(getenv('CHAT_ID')) # type: ignore

user_router = Router()

class Report(StatesGroup):
    create_repost = State()

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

@user_router.message(F.text == ReplyTextCommand.DELETE)
async def all_delete_note(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Создание сброшено', reply_markup=create_note)
    
@user_router.message(F.text == ReplyTextCommand.REPORT_BUG)
async def report_bug(message: types.Message, state: FSMContext):
    await message.answer('Опишите что произошло', reply_markup=create_note)
    await state.set_state(Report.create_repost)

@user_router.message(Report.create_repost)
async def message_bug(message: types.Message, state: FSMContext):
    user_report = await message.answer(
        f'#Ошибка\n\n<i>{message.text}</i>\n\n<b>Сообщил пользователь</b>: @{message.from_user.username}',
        parse_mode='HTML')
    await message.bot.copy_message(
        chat_id=CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=user_report.message_id)
    await message.answer('Ошибка опубликована', reply_markup=create_note)
    await state.clear()
