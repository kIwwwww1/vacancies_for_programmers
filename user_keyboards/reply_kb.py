from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ReplyTextCommand:
    CREATE_RESUME = 'Создать резюме'
    CREATE_VACANCY = 'Создать вакансию'
    DELETE = 'Сбросить все'
    REPORT_BUG = 'Сообщить об ошибке'

create_note = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=ReplyTextCommand.CREATE_RESUME)],
    [KeyboardButton(text=ReplyTextCommand.CREATE_VACANCY)],
    [KeyboardButton(text=ReplyTextCommand.REPORT_BUG)]
], resize_keyboard=True)

delete_resume_or_vacancy = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=ReplyTextCommand.DELETE)]], resize_keyboard=True)