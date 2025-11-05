from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

create_note = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать запись')]
], resize_keyboard=True)