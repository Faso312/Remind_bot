import asyncio, logging
from aiogram import Bot, Dispatcher
from handlers import dispatcher, help, run
from handlers.database import token, timestep, get_values, reply, def_time


logging.basicConfig(level=logging.INFO)

# Настройка бота
bot = Bot(token)
dp = Dispatcher()


async def sending(): #функция цикличной рассылки оповещений
    try:
        while True:
            data_list=timestep(get_values(), def_time) #присваевыем значение функции локальному списку
            for routs in data_list:
                for user_id in set(routs[2]): 
                    if user_id:await bot.send_message(chat_id=int(user_id), 
                                            text=f'{reply[0]} {routs[0]}{reply[1]} {routs[1]} {reply[2]}')
            await asyncio.sleep(1920) #проверка каждые __ секунд --- 1920 - 32 мин
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
            tasks_list = [event_loop.create_task(sending()), event_loop.create_task(main())] #список поручений
            wait_tasks = asyncio.wait(tasks_list) #ожидание выпонения
            event_loop.run_until_complete(wait_tasks) #асинхронное выпонение
except KeyboardInterrupt as e: 
    event_loop.close() #закрытие
    print(f'Работа приостановлена......') #прерывание через Ctrl+C
except Exception as e: print(f'Ошибка вида: {e}.....') #общая обработа ошибок
