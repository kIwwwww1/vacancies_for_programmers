from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ReplyTextCommand:
    CREATE_NOTE = 'Создать запись'

create_note = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=ReplyTextCommand.CREATE_NOTE)]
], resize_keyboard=True)
