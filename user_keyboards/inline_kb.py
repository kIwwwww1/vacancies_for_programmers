from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineTextCommand:
    RESET_NOTE = 'Сбросить все'

reset_note = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=InlineTextCommand.RESET_NOTE, callback_data='reset_note')]
])