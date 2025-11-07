from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from user_keyboards.reply_kb import ReplyTextCommand
from user_keyboards.inline_kb import action_from_note_resume
from database_config.database_setting import create_session, User
from user_keyboards.reply_kb import ReplyTextCommand, delete_resume_or_vacancy, create_note
from .main_commands import CHAT_ID

resume_router = Router()

class CreateResume(StatesGroup):
    await_form_work = State()
    await_employment = State()
    await_salary = State()  
    await_contacts = State()
    await_about_me = State()
    await_stack = State()
    await_additionally = State()


@resume_router.message(F.text == ReplyTextCommand.CREATE_RESUME)
async def create_resume_command(message: types.Message, state: FSMContext):
    await message.answer(
        '<b>Введите желаемый формат работы</b>\n'
        'Пример: <i>Удалённо</i>',
        parse_mode='HTML',
        reply_markup=delete_resume_or_vacancy
    )
    await state.set_state(CreateResume.await_form_work)


@resume_router.message(CreateResume.await_form_work)
async def process_form_work(message: types.Message, state: FSMContext):
    await state.update_data(form_work=message.text.capitalize())
    await message.answer(
        '<b>Укажите тип занятости</b>\n'
        'Пример: <i>Полная / Частичная/Полная / Проектная</i>',
        parse_mode='HTML'
    )
    await state.set_state(CreateResume.await_employment)


@resume_router.message(CreateResume.await_employment)
async def process_employment(message: types.Message, state: FSMContext):
    await state.update_data(employment=message.text.title())
    await message.answer(
        '<b>Укажите ожидаемую оплату</b>\n'
        'Пример: <i>От 1600₽ в день / 90000₽ в месяц</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_salary)


@resume_router.message(CreateResume.await_salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await message.answer(
        '<b>Укажите ваши контакты</b>\n'
        'Пример: <i>Telegram / Email / GitHub</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_contacts)


@resume_router.message(CreateResume.await_contacts)
async def process_contacts(message: types.Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    await message.answer(
        '<b>Расскажите немного о себе</b>\n'
        'Пример: <i>Создаю Telegram-ботов на Python под любые задачи...</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_about_me)


@resume_router.message(CreateResume.await_about_me)
async def process_about_me(message: types.Message, state: FSMContext):
    await state.update_data(about_me=message.text)
    await message.answer(
        '<b>Укажите ваш стек технологий через # и ,</b>\n'
        'Пример: <i>#Python, #Aiogram, #SQL, #JS</i>', parse_mode='HTML')
    await state.set_state(CreateResume.await_stack)


@resume_router.message(CreateResume.await_stack)
async def process_stack(message: types.Message, state: FSMContext):
    await state.update_data(stack=message.text.title())
    data = await state.get_data()
    resume_text = (
        f"#резюме\n\n"
        f"<b>Формат работы:</b> #{data.get('form_work', '')}\n"
        f"<b>Занятость:</b> #{data.get('employment', '')}\n"
        f"<b>Ожидания по зарплате:</b> {data.get('salary', '')}\n"
        f"<b>Обо мне:</b>\n{data.get('about_me', '')}\n\n"
        f"<b>Контакты:</b> {data.get('contacts', '')}\n\n"
        f"<b>Стек:</b> {data.get('stack', '')}")
    user_response = await message.answer(resume_text, parse_mode='HTML')
    await state.update_data(resume_message_id=user_response.message_id)
    await message.answer('Предпросмотр резюме', reply_markup=action_from_note_resume)


@resume_router.callback_query(F.data == 'create_user_note_resume')
async def add_resume(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.delete()
    await callback.bot.copy_message(
        chat_id=CHAT_ID, 
        from_chat_id=callback.message.chat.id, 
        message_id=user_data['resume_message_id'])
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=user_data['resume_message_id'])
    await state.clear()
    await callback.message.answer('Резюме создано и опубликовано ✅', reply_markup=create_note)


@resume_router.callback_query(F.data == 'reset_user_note_resume')
async def delete_resume(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Резюме удалено ❌', reply_markup=create_note)
    await state.clear()
