from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.static_kb import get_choice_keyboard
from .database import greeting


router = Router()

@router.message(Command('start','choice','menu','help'))
async def cmd_start_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Привет, {message.chat.first_name}! {greeting[0]}',reply_markup=get_choice_keyboard())






