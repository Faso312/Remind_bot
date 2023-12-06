from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from .database import *
from keyboards.dinemic_kb import make_row_keyboard





router = Router()

class Admin(StatesGroup):
    secret_key=State()
    hours=State()

class Steps(StatesGroup):
    step1=State()
    step2=State()

class Assign_route(StatesGroup):
    ID=State()
    route=State()

class Route_list(StatesGroup):
    route_ID=State()

class User_data(StatesGroup):
    ID=State()
    name=State()
    pf_number=State()



@router.callback_query(F.data == 'reg')
async def registration(callback: types.CallbackQuery, state: FSMContext): 
    await state.clear()
    await callback.message.answer(f'{user_int[2]}',reply_markup=ReplyKeyboardRemove())
    await state.set_state(User_data.ID)
    await callback.answer() #чистка оперативной памяти

@router.message(User_data.ID,F.text)
async def reg_step1(message: Message, state: FSMContext):
    if len(message.text) == 11:
        data_list=check_in_route(str(message.text),get_routes())[0]
        if data_list: #list
            await message.answer(f'{user_int[0]}',reply_markup=ReplyKeyboardRemove())
            register_user([message.from_user.id,data_list[3],data_list[4],data_list[1],data_list[0]])
            await state.clear()
        else: #none
            await message.answer(f'{user_int[1]}',reply_markup=ReplyKeyboardRemove())
            await state.set_state(User_data.ID)
    else:
        await message.answer(f'Неправильная форма ввода, попробуйте снова',reply_markup=ReplyKeyboardRemove())
        await state.set_state(User_data.ID) #Устанавливаем пользователю состояние - "выбирает ответ"

@router.callback_query(F.data == 'my_routs')
async def my_routs(callback: types.CallbackQuery, state: FSMContext): 
    await state.clear()
    await callback.message.answer(f'Отлично, нажмите для просмотра⚡',reply_markup=make_row_keyboard(routs_kb))
    await state.set_state(Route_list.route_ID)
    await callback.answer() #чистка оперативной памяти

@router.message(Route_list.route_ID,F.text)
async def my_routs1(message: Message, state: FSMContext):
    try:
        await message.answer(f'Ваши мероприятия',reply_markup=ReplyKeyboardRemove())
        for itr in get_user_routs(message.from_user.id): await message.answer(f'{itr}')
        await state.clear()
    except AttributeError:
        await message.answer(f'Для начала пройдите регистрацию')
        await state.clear()



#except
@router.message(Steps.step1)
async def wrong_answer1(message: Message):  #проверка ответов
    await message.answer(f'Нажмите для продолжения',reply_markup=make_row_keyboard(routs_kb))
