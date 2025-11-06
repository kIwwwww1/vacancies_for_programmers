from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from user_keyboards.reply_kb import ReplyTextCommand
from user_keyboards.inline_kb import action_from_note
from .main_commands import CHAT_ID

vacancy_router = Router()

class CreateNote(StatesGroup):
    await_title = State()
    await_type_of_employment = State()
    await_user_level = State()
    await_location = State()
    await_country = State()
    await_responsibilities = State()
    await_requirements = State()
    await_mb_plus = State()
    await_additionally = State()
    await_contacts = State()
    await_stack = State()


@vacancy_router.message(F.text == ReplyTextCommand.CREATE_VACANCY)
async def create_vacancy_command(message: types.Message, state: FSMContext):
    await message.answer(
        '<b>Укажите название для вакансии</b>\n'
        'Пример: <i>Junior Python Developer</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_title)


@vacancy_router.message(CreateNote.await_title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        '<b>Укажите тип занятости</b>\n'
        'Пример: <i>Full-time, Part-time, Internship</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_type_of_employment)


@vacancy_router.message(CreateNote.await_type_of_employment)
async def process_type_of_employment(message: types.Message, state: FSMContext):
    await state.update_data(type_of_employment=message.text)
    await message.answer(
        '<b>Укажите уровень пользователя</b>\n'
        'Пример: <i>Junior, Middle, Senior</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_user_level)


@vacancy_router.message(CreateNote.await_user_level)
async def process_user_level(message: types.Message, state: FSMContext):
    await state.update_data(user_level=message.text)
    await message.answer(
        '<b>Укажите локацию</b>\n'
        'Пример: <i>Moscow, Remote</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_location)


@vacancy_router.message(CreateNote.await_location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer(
        '<b>Укажите страну</b>\n'
        'Пример: <i>RU, USA, UK</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_country)


@vacancy_router.message(CreateNote.await_country)
async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await message.answer(
        '<b>Укажите обязанности</b>\n'
        'Пример: <i>Разработка бэкенда, участие в проектах</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_responsibilities)


@vacancy_router.message(CreateNote.await_responsibilities)
async def process_responsibilities(message: types.Message, state: FSMContext):
    await state.update_data(responsibilities=message.text)
    await message.answer(
        '<b>Укажите требования</b>\n'
        'Пример: <i>Знание Python, опыт работы с Django</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_requirements)


@vacancy_router.message(CreateNote.await_requirements)
async def process_requirements(message: types.Message, state: FSMContext):
    await state.update_data(requirements=message.text)
    await message.answer(
        '<b>Укажите, что будет плюсом</b>\n'
        'Пример: <i>Знание FastAPI, опыт работы с Docker</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_mb_plus)


@vacancy_router.message(CreateNote.await_mb_plus)
async def process_mb_plus(message: types.Message, state: FSMContext):
    await state.update_data(mb_plus=message.text)
    await message.answer(
        '<b>Укажите дополнительную информацию</b>', parse_mode='HTML')
    await state.set_state(CreateNote.await_additionally)


@vacancy_router.message(CreateNote.await_additionally)
async def process_additionally(message: types.Message, state: FSMContext):
    await state.update_data(additionally=message.text)
    await message.answer(
        '<b>Укажите контакты</b>\n'
        'Пример: <i>telegram: @username, email: example@mail.com</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_contacts)


@vacancy_router.message(CreateNote.await_contacts)
async def process_contacts(message: types.Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    await message.answer(
        '<b>Укажите стек технологий</b>\n'
        'Пример: <i>Python, Django, PostgreSQL</i>', parse_mode='HTML')
    await state.set_state(CreateNote.await_stack)


@vacancy_router.message(CreateNote.await_stack)
async def process_stack(message: types.Message, state: FSMContext):
    await state.update_data(stack=message.text)
    data = await state.get_data()
    user_response = await message.answer(
            f'{data["title"]}\n\n'
            f'Тип занятости: #{data["type_of_employment"]}\n'
            f'Уровень: #{data["user_level"]}\n'
            f'Страна: #{data.get("country", "RU")}\n'
            f'Локация: #{data["location"]}\n\n'
            f'{data["title"]}\n\n'
            f'<b>Обязанности</b>\n'
            f'{data["responsibilities"]}\n\n'
            f'<b>Требования</b>\n'
            f'{data["requirements"]}\n\n'
            f'<b>Будет плюсом</b>\n'
            f'{data["mb_plus"]}\n\n'
            f'<b>Что предлагаем</b>\n'
            f'{data["additionally"]}\n\n'
            f'<b>Контакты</b>\n'
            f'{data["contacts"]}\n\n'
            f'⚠️ Для удобства указывайте ссылку на вакансию\n'
            # f'Ссылка: {data.get("vacancy_link", "—")}\n\n'
            f'Стек технологий: {data["stack"]}',parse_mode='HTML')
    await state.update_data(vacancy_message_id=user_response.message_id)
    await message.answer('Предпросмотр вакансии', reply_markup=action_from_note)


@vacancy_router.callback_query(F.data == 'create_user_note')
async def add_note(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.answer('Создание вакансии...')
    await callback.message.delete()
    await callback.bot.copy_message(chat_id=CHAT_ID,
                                    from_chat_id=callback.message.chat.id ,
                                    message_id=user_data['vacancy_message_id'])
    await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=user_data['vacancy_message_id'])
    await state.clear()


@vacancy_router.callback_query(F.data == 'reset_user_note')
async def delete_note(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Вакансия удалена')
    await state.clear()
