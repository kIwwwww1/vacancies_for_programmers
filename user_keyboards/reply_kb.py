from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ReplyTextCommand:
    CREATE_RESUME = 'Создать резюме'
    CREATE_VACANCY = 'Создать вакансию'
    BUY_TOKEN = 'Купить токен'

create_note = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=ReplyTextCommand.CREATE_RESUME)],
    [KeyboardButton(text=ReplyTextCommand.CREATE_VACANCY)]
], resize_keyboard=True)
