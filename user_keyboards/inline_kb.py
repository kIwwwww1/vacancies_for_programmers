from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineTextCommand:
    RESET_NOTE = 'Сбросить все'
    CREATE_USER_NOTE = 'Создать'

action_from_note = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=InlineTextCommand.RESET_NOTE, callback_data='reset_user_note')],
    [InlineKeyboardButton(text=InlineTextCommand.CREATE_USER_NOTE, callback_data='create_user_note')]
])