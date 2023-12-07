import gspread, time
from datetime import datetime


greeting = ['👋 Я здесь, чтобы помочь вам с рассылкой оповещений о собраниях. Со мной вы сможете эффективно организовать свои собрания и держать свою команду в курсе всех важных событий😊']
reply=['Здравствуйте, ','!\nНапоминаю вам о предстоящем мероприятии: ','📅\nБудем рады вас видеть🤗👋', 'Ваши мероприятияна следущую неделю']
user_int=['Регистрация прошла успешно, теперь вы будете получать уведомления📅🎉','Ваш номер не найден в базе данных, попробуйте еще раз или обратитесь за помощью к администратору','Отлично, начнем регистрацию⚡\nВведите свой номер в формате: 89271234567']
token='6836856781:AAGtxQPztvNP_ClUNMqGHnpwIwWWdcvUNTE'
routs_kb=['Мероприятия']
def_time=6 #базовое время оповещения

secret_key = gspread.service_account('Key.json') #подключение в json файлу библиотеки
sh = secret_key.open("Remind_me_bot") #открытие таблицы с таким-то названием
sh1=sh.get_worksheet(0) #определение рабочей страницы в таблице
sh2=sh.get_worksheet(1) #определение рабочей страницы в таблице

def on_hold(seconds: int): #задержка для передачи излишних запросов серверу
    retry_after = seconds  #повторная попытка после __ секунд
    time.sleep(retry_after) 

def check_in_route(phone_number: str, list_ : list): #возврат значений юзера
    return [itr[itr.index(str(phone_number))-4:itr.index(str(phone_number))+1] for itr in list_ if str(phone_number) in itr]

def get_routes() -> list[list]: #все значения стр. "Мероприятия"
    try: return sh2.get_values()[2:] #вывод общего списка мероприятий
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_routes()
    
def get_users() -> list[list]: #все значения стр. "Пользователи"
    try: return sh1.get_values()[1:] #вывод общего списка мероприятий
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_users()

def register_user(user_data: list): #регистрация пользователя
    try:
        last_row = len(sh1.get_all_values()) + 1 #получение последнего значения заполненной строки +1 
        for col in range(1, len(user_data)+1): #заполнение (1, длинна списка ответов)
            sh1.update_cell(last_row, col, user_data[col-1]) #определяем место ввода(последняя свободная, столбец, значение)
    except gspread.exceptions.APIError:
        on_hold(30)
        return register_user(user_data)
        
def check(list_: str, elenemt: str): #проверка на наличие в списке
    for itr in list_:  
        if elenemt in itr: 
            return True
        else: return False

def timestep(timetable: list, def_time: int) -> list: #получение id для рассылки
    curent_time=datetime.now() #текущее время без миллисекунд
    time_list=[] #локальный список мероприятий
    for itr in timetable: 
        route_time = datetime.strptime(itr[4], "%d.%m.%Y %H:%M:%S") #строку во время
        dif_dates=curent_time - route_time #дни между числами
        dif_time=int(dif_dates.total_seconds()/60/60) #часы между числами
        print(dif_time)
        if dif_time == -int(def_time) or dif_time == -1: time_list.extend([[itr[0],itr[1],itr[4]]])
    return time_list #вывод списка id с названием 

def check_for_day(day: int, hour_ : int) ->bool: 
    if int(day)-1 == datetime.today().weekday() and datetime.today().hour == int(hour_): return True
    else: return False

def routs_to_come(timetable: list) -> list: #список запланированных мероприятий
    curent_time=datetime.now()
    time_list=[] #локальный список мероприятий
    for itr in tuple(timetable): 
        route_time = datetime.strptime(itr[1], "%d.%m.%Y %H:%M:%S") #строку во время
        dif_dates=curent_time - route_time #дни между числами
        dif_time=int(dif_dates.total_seconds()/60/60) #часы между числами
        if dif_time <0: time_list.append(itr) #вывод списка id с названием
    return time_list

def get_user_routs(user_id: str, list_:list) ->list: #мероприятия пользователя
    try: return [[user[0],user[4]] for user in list_ if user[0] == str(user_id)]
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_user_routs(user_id,list_)
    except Exception as e: print(f'Ошибка: {e}')

def get__routs(list_:list) ->list: #мероприятия пользователя
    try: return [[user[0],user[4]] for user in list_]
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_user_routs(list_)
    except Exception as e: print(f'Ошибка: {e}')


    







