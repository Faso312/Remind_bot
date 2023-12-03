from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_choice_keyboard():
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Регистрация', callback_data='reg')
    buttons.button(text='Записаться', callback_data='assign')
    buttons.button(text='Мои мероприятия', callback_data='my_routs')
    buttons.button(text='Администратору', callback_data='admin')
    buttons.adjust(2)
    return buttons.as_markup()

def get_admin_keyboard():
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Мероприятия', callback_data='routs')
    buttons.button(text='Часы до отправки оповещений', callback_data='update')
    buttons.adjust(1)
    return buttons.as_markup()


    

