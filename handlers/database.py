import gspread, time
from datetime import datetime


greeting = ['👋 Я здесь, чтобы помочь тебе с рассылкой оповещений о собраниях. Со мной ты сможешь эффективно организовать свои собрания и держать свою команду в курсе всех важных событий. Что мне для тебя сделать сегодня? 😊']
reply=['Привет! 🤖\nХочу напомнить тебе о предстоящем мероприятии :','! 📅🎉\nМы будем рады видеть тебя','\nЖдем встречи с нетерпением! 🤗✨']
user_int=['Как к вам обращаться?','Пожалуйста, оставьте свой номер телефона', 'Выберите мероприятие из списка']
token='6836856781:AAGtxQPztvNP_ClUNMqGHnpwIwWWdcvUNTE'
register=['Пройти регистрацию']
routs_kb=['Мероприятия']
key='93af5b01dc'
def_time=5 #базовое время оповещения


secret_key = gspread.service_account('Key.json') #подключение в json файлу библиотеки
sh = secret_key.open("Vote_data") #открытие таблицы с таким-то названием
sh9=sh.get_worksheet(9) #определение рабочей страницы в таблице
sh10=sh.get_worksheet(10) #определение рабочей страницы в таблице

def change_time(hours: int): #функция, опр кол-ло часов перед уведомлением пользователя
    global def_time
    def_time=int(hours)

def on_hold(seconds: int): #задержка для передачи излишних запросов серверу
    retry_after = seconds  #повторная попытка после __ секунд
    time.sleep(retry_after) 

def get_routs() -> list: #мероприятия
    try: return sh10.col_values(2)[1:] #вывод общего списка мероприятий
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_routs()[1:]
    
def get_values() -> list: #все значения листа
    try: return sh10.get_all_values()[1:] #общий вывод
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_values()[1:]
    
def get_user_data_if_registered(user_id : str) -> list: #педечача данные, если id  в системе
    try: return sh9.row_values(sh9.find(str(user_id)).row)
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_user_data_if_registered(user_id)
    
def get_candidats() -> list: #пользователи
    try: return sh.get_worksheet(9).get_all_values()[1:] #вывод общего списка кандидатов
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_candidats()[1:]
    
def check_for_id(user_id: str): #проверка на наличие в списке
    try:
        if str(user_id) not in sh.get_worksheet(9).col_values(1): return True #проверка на наличие id
        else: return False
    except gspread.exceptions.APIError:
        on_hold(30)
        return check_for_id(user_id)

def timestep(timetable: list, def_time: int) -> list: #получение id для рассылки
    curent_time=datetime.now().replace(microsecond=0, tzinfo=None) #текущее время без миллисекунд
    time_list=[] #локальный список мероприятий
    for itr in timetable: 
        route_time = datetime.strptime(itr[2], "%d/%m/%Y %H:%M") #строку во время
        dif_dates=curent_time - route_time #дни между числами
        dif_time=int(dif_dates.total_seconds()/60/60) #часы между числами
        if dif_time == -int(def_time): time_list.extend([[itr[1],itr[2],itr[3].split(' ')]])
        elif dif_time == -1: time_list.extend([[itr[1],itr[2],itr[3].split(' ')]])
    return time_list #вывод списка id с названием 

def registration_user(user_data: list): #регистрауия пользователя
    try:
        last_row = len(sh9.get_all_values()) + 1 #получение последнего значения заполненной строки +1 
        for col in range(1, len(user_data)+1): #заполнение (1, длинна списка ответов)
            sh9.update_cell(last_row, col, user_data[col-1]) #определяем место ввода(последняя свободная, столбец, значение)
    except gspread.exceptions.APIError:
        on_hold(30)
        return registration_user(user_data)
    
def apply_route(user_data: list): #запись на мероприятие
    try:
        data=f'{str(user_data[1])} {str(user_data[2])}'
        new_value_route=sh10.cell(sh10.find(str(user_data[1])).row,4).value + ' ' + str(user_data[0]) #добавление id в ячейку
        sh10.update_cell(sh10.find(str(user_data[1])).row, 4, str(new_value_route)) #добавление новых значений
        new_value_user=sh9.cell(sh9.find(str(user_data[0])).row,4).value + ',' + str(data) #добавление мероприятия в ячейку
        sh9.update_cell(sh9.find(str(user_data[0])).row, 4, str(new_value_user)) #добавление новых значений
    except gspread.exceptions.APIError:
        on_hold(30)
        return apply_route(user_data)
    except TypeError:
        sh10.update_cell(sh10.find(str(user_data[1])).row, 4, str(user_data[0])) #добавление новых значений
        sh9.update_cell(sh9.find(str(user_data[0])).row, 4, str(data)) #добавление новых значений
    #except AttributeError: return apply_route(user_data)
    
def routs_to_come_admin(timetable: list) -> list: #список запланированных мероприятий
    routs_to_come_list=[] #локальный список запланированных мероприятий
    curent_time=datetime.now().replace(microsecond=0, tzinfo=None) #текущее время без миллисекунд
    for itr in timetable: 
        route_time = datetime.strptime(itr[2], "%d/%m/%Y %H:%M") #строку во время
        dif_dates=curent_time - route_time #дни между числами
        dif_time=int(dif_dates.total_seconds()/60/60) #часы между числами
        if dif_time <0: routs_to_come_list.extend([[itr[1],itr[2]]]) #вывод списка id с названием
    return  routs_to_come_list

def get_user_routs(user_id: str) ->list: #мероприятия пользователя
    try: 
        return set(sh9.cell(sh9.find(str(user_id)).row,4).value.split(','))
    except gspread.exceptions.APIError:
        on_hold(5)
        return get_user_routs(user_id)
    






