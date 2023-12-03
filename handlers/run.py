from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from .database import *
from keyboards.dinemic_kb import make_row_keyboard
from keyboards.static_kb import get_admin_keyboard


routs_kb=['Мероприятия']

router = Router()

class Admin(StatesGroup):
    secret_key=State()
    hours=State()

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
    await callback.message.answer(f'Отлично, начнем регистрацию⚡',reply_markup=make_row_keyboard(register))
    await state.set_state(User_data.ID)
    await callback.answer() #чистка оперативной памяти

@router.message(User_data.ID,F.text.in_(register))
async def reg_step1(message: Message, state: FSMContext):
    if check_for_id(message.from_user.id) is True:
        await message.answer(f'{user_int[0]}',reply_markup=ReplyKeyboardRemove())
        await state.set_state(User_data.name) #Устанавливаем пользователю состояние - "выбирает ответ"
    else:
        await message.answer(f'Вы уже зарегистрированы\n{user_int[2]}',reply_markup=ReplyKeyboardRemove())
        routs = routs_to_come_admin(get_values())
        for rout in routs: await message.answer(f'{routs.index(rout)+1}. {rout[0]}: {rout[1]}')
        await message.answer(f'Введите порядковый номер мероприятия, которое хотите посетить',reply_markup=ReplyKeyboardRemove())
        await state.set_state(Assign_route.route) #Устанавливаем пользователю состояние - выбирает ответ"

@router.message(User_data.name,F.text)
async def reg_step1(message: Message, state: FSMContext):
    await state.update_data(user_ID=message.from_user.id,user_name=message.text)
    await message.answer(f'{user_int[1]}')
    await state.set_state(User_data.pf_number) #Устанавливаем пользователю состояние - выбирает ответ"

@router.message(User_data.pf_number,F.text)
async def reg_step2(message: Message, state: FSMContext):
    await state.update_data(user_number=message.text)
    await message.answer(f'Регистрация прошла успешно',reply_markup=ReplyKeyboardRemove())
    user_data = await state.get_data()
    registration_user(list(user_data.values()))
    await state.clear()

@router.callback_query(F.data == 'assign')
async def call_asign(callback: types.CallbackQuery, state: FSMContext):
    await state.clear() #чистка класса
    if check_for_id(callback.message.from_user.id) is False:
        await callback.message.answer(f'{user_int[0]}',reply_markup=ReplyKeyboardRemove())
        await state.set_state(User_data.name) #Устанавливаем пользователю состояние - "выбирает ответ"
    else: 
        await callback.message.answer(f'{user_int[2]}',reply_markup=ReplyKeyboardRemove())
        routs = routs_to_come_admin(get_values())
        for rout in routs: await callback.message.answer(f'{routs.index(rout)+1}. {rout[0]}: {rout[1]}')
        await callback.message.answer(f'Введите порядковый номер мероприятия, которое хотите посетить',reply_markup=ReplyKeyboardRemove())
        await state.set_state(Assign_route.route) #Устанавливаем пользователю состояние - выбирает ответ"
        await callback.answer() #чистка оперативной памяти
        


@router.message(Assign_route.route,F.text)
async def assign_route(message: Message, state: FSMContext):
    await state.update_data(user_ID=message.from_user.id,route=message.text)
    routs = routs_to_come_admin(get_values())
    apply_route([message.from_user.id, str(routs[int(message.text)-1][0]),str(routs[int(message.text)-1][1])])
    await message.answer(f'Запись прошла успешно',reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.callback_query(F.data == 'my_routs')
async def registration(callback: types.CallbackQuery, state: FSMContext): 
    await state.clear()
    await callback.message.answer(f'Отлично, нажмите для просмотра⚡',reply_markup=make_row_keyboard(routs_kb))
    await state.set_state(Route_list.route_ID)
    await callback.answer() #чистка оперативной памяти

@router.message(Route_list.route_ID,F.text)
async def reply_route(message: Message, state: FSMContext):
    await message.answer(f'Ваши мероприятия',reply_markup=ReplyKeyboardRemove())
    for itr in get_user_routs(message.from_user.id): await message.answer(f'{itr}')
    await state.clear()

@router.callback_query(F.data == 'admin')
async def call_admin(callback: types.CallbackQuery, state: FSMContext):
    await state.clear() #чистка класса
    await callback.message.answer(f'Введите ключ авторизации',reply_markup=ReplyKeyboardRemove())
    await callback.answer() #чистка оперативной памяти



@router.message(Admin.secret_key,F.text)
async def try_key(message: Message, state: FSMContext):
    if message.text == key:
        await message.answer(f'Начнем работу👨‍💻',reply_markup=get_admin_keyboard())
        await state.clear()
    else: 
        await message.answer(f'Ключ введен неверно😔',reply_markup=ReplyKeyboardRemove())
        await state.clear()

@router.callback_query(F.data == 'update')
async def call_update(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f'🕓За сколько часов мне оповещать пользователей?🕓',reply_markup=ReplyKeyboardRemove())
    await state.set_state(Admin.hours) #Устанавливаем пользователю состояние - выбирает ответ"
    await callback.answer() #чистка оперативной памяти

@router.message(Admin.hours,F.text)
async def hours__update(message: Message, state: FSMContext):
    change_time(int(message.text))
    await message.answer(f'🕓Отлично, теперь оповещения будут приходить за {message.text} часов и за час до начала🕓',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.callback_query(F.data == 'routs')
async def call__routs(callback: types.CallbackQuery, state: FSMContext):
    for itr in routs_to_come_admin(get_values()):
        await callback.message.answer(f'Запланированные мероприятия: \n{itr}',reply_markup=ReplyKeyboardRemove())
    await callback.answer() #чистка оперативной памяти
    await state.clear()



    