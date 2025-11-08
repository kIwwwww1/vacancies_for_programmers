from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineTextCommand:
    RESET_NOTE = 'Сбросить все'
    CREATE_USER_NOTE = 'Создать'
    RESET_NOTE_RESUME = 'Сбросить все'
    CREATE_USER_NOTE_RESUME = 'Создать'
    REPORT = 'Пожаловаться 😠'
    CREATE = 'Создать для себя 🤖'


action_from_note = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=InlineTextCommand.RESET_NOTE, callback_data='reset_user_note')],
    [InlineKeyboardButton(text=InlineTextCommand.CREATE_USER_NOTE, callback_data='create_user_note')]
])

action_from_note_resume = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=InlineTextCommand.RESET_NOTE, callback_data='reset_user_note_resume')],
    [InlineKeyboardButton(text=InlineTextCommand.CREATE_USER_NOTE, callback_data='create_user_note_resume')]
])

report_message = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=InlineTextCommand.REPORT, url='https://t.me/Receiver_of_God')]
])

report_and_create_message = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=InlineTextCommand.CREATE, url='https://t.me/IT_Jobs_Officially_Bot')],
    [InlineKeyboardButton(text=InlineTextCommand.REPORT, url='https://t.me/Receiver_of_God')]
])