from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_choice_keyboard():
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Регистрация', callback_data='reg')
    buttons.button(text='Отключить уведомления', callback_data='unreg')
    buttons.button(text='Мои мероприятия', callback_data='my_routs')
    buttons.adjust(2)
    return buttons.as_markup()



    

