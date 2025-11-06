from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from user_keyboards.reply_kb import ReplyTextCommand
from user_keyboards.inline_kb import reset_note

vacancy_router = Router()

class CreateNote(StatesGroup):
    await_title = State()
    await_location = State()

@vacancy_router.message(F.text == ReplyTextCommand.CREATE_VACANCY)
async def create_vacancy_command(message: types.Message, state: FSMContext):
    await message.answer(
        f'<b>Укажите название для вакансии</b>\n'
        f'Пример: <i>"Junior Python Developer"</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_title)

@vacancy_router.message(CreateNote.await_title)
async def wait_title_for_vacancy(message: types.Message, state: FSMContext):
    print(message.text)
    await state.clear()

    
@vacancy_router.message(F.text == ReplyTextCommand.CREATE_RESUME)
async def create_resume_command(message: types.Message, state: FSMContext):
    await message.answer('РЕЗЮМЕ')


# Сделать что бы 1 резюме можно было вылоить бесплатно, 
# что бы выложить второе резюме или вакансию надо заплатить