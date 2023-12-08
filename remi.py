import asyncio,logging
from aiogram import Bot,Dispatcher
from handlers import dispatcher,help,run
from handlers.database import *


logging.basicConfig(level=logging.INFO)

# Настройка бота
bot = Bot(token)
dp = Dispatcher()

async def sending_sunday(): #функция цикличной рассылки оповещений
    try:
        while True:
            if check_for_day(6,8) is True:
                data_list=routs_to_come(get__routs(get_users())) #присваевыем значение функции локальному списку
                for itr in data_list: 
                    if itr:
                        await bot.send_message(chat_id=int(itr[0]),text=f'{reply[3]}\n - {itr[1]}')
            await asyncio.sleep(2400) #проверка каждые __ секунд --- 2400 - 40 мин
    except KeyboardInterrupt: pass

async def sending(): #функция цикличной рассылки оповещений
    try:
        while True:
            data_list=timestep(get_users(),def_time) #присваевыем значение функции локальному списку
            for rout in data_list:
                    if rout:await bot.send_message(chat_id=int(rout[0]), text=f'{reply[0]}{rout[1]}{reply[1]}{rout[2]}{reply[2]}')
            await asyncio.sleep(2400) #проверка каждые __ секунд --- 2400 - 40 мин
    except KeyboardInterrupt: pass

async def main(): #основная функция системы
    dp.include_router(dispatcher.router)
    dp.include_router(run.router)
    dp.include_router(help.router) 
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    
try: #последователльная обработка функциий
    if __name__ == '__main__': 
            event_loop = asyncio.get_event_loop() #цикл событий
            tasks_list = [event_loop.create_task(sending()),event_loop.create_task(sending_sunday()), 
                          event_loop.create_task(main())] #список поручений
            wait_tasks = asyncio.wait(tasks_list) #ожидание выпонения
            event_loop.run_until_complete(wait_tasks) #асинхронное выпонение
except KeyboardInterrupt as e: 
    event_loop.close() #закрытие
    print(f'Работа приостановлена......') #прерывание через Ctrl+C
except Exception as e: print(f'Ошибка вида: {e}.....') #общая обработа ошибок
