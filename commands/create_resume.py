from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from user_keyboards.reply_kb import ReplyTextCommand
from user_keyboards.inline_kb import action_from_note_resume
from database_config.database_setting import create_session, User
from user_keyboards.reply_kb import ReplyTextCommand, delete_resume_or_vacancy
from .main_commands import CHAT_ID

resume_router = Router()

class CreateResume(StatesGroup):
    await_name = State()
    await_age = State()
    await_position = State()
    await_location = State()
    await_country = State()
    await_experience = State()
    await_education = State()
    await_skills = State()
    await_about = State()
    await_contacts = State()
    await_stack = State()


@resume_router.message(F.text == ReplyTextCommand.CREATE_RESUME)
async def create_resume_command(message: types.Message, state: FSMContext):
    await message.answer(
        '<b>Введите ваше имя и фамилию</b>\n'
        'Пример: <i>Иван Иванов</i>', parse_mode='HTML', reply_markup=delete_resume_or_vacancy)
    await state.set_state(CreateResume.await_name)


@resume_router.message(CreateResume.await_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        '<b>Укажите ваш возраст</b>\n'
        'Пример: <i>25 лет</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_age)


@resume_router.message(CreateResume.await_age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(
        '<b>Укажите желаемую должность</b>\n'
        'Пример: <i>Python Developer</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_position)


@resume_router.message(CreateResume.await_position)
async def process_position(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer(
        '<b>Укажите вашу локацию</b>\n'
        'Пример: <i>Moscow, Remote</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_location)


@resume_router.message(CreateResume.await_location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer(
        '<b>Укажите вашу страну</b>\n'
        'Пример: <i>RU, USA, UK</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_country)


@resume_router.message(CreateResume.await_country)
async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await message.answer(
        '<b>Опишите ваш опыт работы</b>\n'
        'Пример: <i>2 года в компании X на позиции Junior Python Developer</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_experience)


@resume_router.message(CreateResume.await_experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer(
        '<b>Укажите образование</b>\n'
        'Пример: <i>МГУ, Факультет ВМК, 2021</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_education)


@resume_router.message(CreateResume.await_education)
async def process_education(message: types.Message, state: FSMContext):
    await state.update_data(education=message.text)
    await message.answer(
        '<b>Укажите ключевые навыки</b>\n'
        'Пример: <i>Python, Django, Git, SQL</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_skills)


@resume_router.message(CreateResume.await_skills)
async def process_skills(message: types.Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await message.answer(
        '<b>Расскажите немного о себе</b>\n'
        'Пример: <i>Ответственный, люблю командную работу, быстро обучаюсь</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_about)


@resume_router.message(CreateResume.await_about)
async def process_about(message: types.Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer(
        '<b>Укажите контакты для связи</b>\n'
        'Пример: <i>telegram: @username, email: example@mail.com</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_contacts)


@resume_router.message(CreateResume.await_contacts)
async def process_contacts(message: types.Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    await message.answer(
        '<b>Укажите стек технологий</b>\n'
        'Пример: <i>Python, FastAPI, PostgreSQL</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_stack)


@resume_router.message(CreateResume.await_stack)
async def process_stack(message: types.Message, state: FSMContext):
    await state.update_data(stack=message.text)
    data = await state.get_data()

    user_response = await message.answer(
        f'<b>{data["name"]}</b>\n'
        f'Возраст: {data["age"]}\n'
        f'Страна: #{data.get("country", "RU")}\n'
        f'Локация: {data["location"]}\n\n'
        f'<b>Позиция:</b> {data["position"]}\n\n'
        f'<b>Опыт работы</b>\n{data["experience"]}\n\n'
        f'<b>Образование</b>\n{data["education"]}\n\n'
        f'<b>Навыки</b>\n{data["skills"]}\n\n'
        f'<b>О себе</b>\n{data["about"]}\n\n'
        f'<b>Контакты</b>\n{data["contacts"]}\n\n'
        f'<b>Стек технологий:</b> {data["stack"]}',
        parse_mode='HTML'
    )

    await state.update_data(resume_message_id=user_response.message_id)
    await message.answer('Предпросмотр резюме', reply_markup=action_from_note_resume)


@resume_router.callback_query(F.data == 'create_user_note_resume')
async def add_resume(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.delete()
    await callback.bot.copy_message(
        chat_id=CHAT_ID,
        from_chat_id=callback.message.chat.id,
        message_id=user_data['resume_message_id']
    )
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=user_data['resume_message_id']
    )
    await state.clear()
    await callback.message.answer('Резюме создано и опубликовано ✅')


@resume_router.callback_query(F.data == 'reset_user_note_resume')
async def delete_resume(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Резюме удалено ❌')
    await state.clear()
