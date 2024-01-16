from PIL import Image
import urllib.request
import requests
from functions.db_functions import *
from functions.sending_functions import *
from config import *
from bot_vars import *
import logging
import time

logging.basicConfig(filename = 'logs.log',  filemode='w', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', datefmt = '%d-%b-%y %H:%M:%S')

def sending(degree, degree_for_sender):

    list_id = search_into_db(degree)

    for id_one in list_id:
        try:
            send(id_one, emojize(f':red_exclamation_mark:Внимание! Значение q - {degree_for_sender}:red_exclamation_mark:'), standart_keyboard)

        except Exception as exception:

            logging.info(f'ПРОБЛЕМЫ С ID {id_one}')
            logging.info(f'Ошибка: {exception}')
            delete_from_db(id_one, True)
            continue

    logging.info(f'Выполнил рассылку уровня {degree}')


def q_degree_return(x_difference, y_difference, z_difference):

    if x_difference >= 1500 or y_difference >= 1500 or z_difference >= 1500:
        return(9)
    elif x_difference >= 990 or y_difference >= 990 or z_difference >= 990:
        return(8)
    elif x_difference >= 600 or y_difference >= 600 or z_difference >= 600:
        return(7)
    elif x_difference >= 360 or y_difference >= 360 or z_difference >= 360:
        return(6)
    elif x_difference >= 210 or y_difference >= 210 or z_difference >= 210:
        return(5)
    elif x_difference >= 120 or y_difference >= 120 or z_difference >= 120:
        return(4)
    elif x_difference >= 60 or y_difference >= 60 or z_difference >= 60:
        return(3)
    elif x_difference >= 30 or y_difference >= 30 or z_difference >= 30:
        return(2)
    elif x_difference >= 15 or y_difference >= 15 or z_difference >= 15:
        return(1)
    else:
        return(0)

# функция проверки графика и высылания ответа с анализом
def graphs_analise(degree, degree_for_sender):

    try:
    
        r = requests.get(url_text, timeout=60)
        data = r.text.split("\n")
        minute_data = data[-900:-1]

        х_deviation = []
        y_deviation = []
        z_deviation = []

        for i in minute_data:
            str(i)
            temp = i.split(' ')
            х_deviation.append(float(temp[-3]))
            y_deviation.append(float(temp[-2]))
            z_deviation.append(float(temp[-1]))

        x_difference = round(max(х_deviation) - min(х_deviation), 3)
        y_difference = round(max(y_deviation) - min(y_deviation), 3)
        z_difference = round(max(z_deviation) - min(z_deviation), 3)

        print(f'Разности: {x_difference}, {y_difference}, {z_difference}')

        q_degree = q_degree_return(x_difference, y_difference, z_difference)

        if q_degree != 0:
            sending(degree, degree_for_sender)

    except:
        print('Connection error')
        time.sleep(1)



# функция проверки графика в данный момент
def graphs_analise_now():
    try:
        r = requests.get(url_text, timeout=60)
        data = r.text.split("\n")
        minute_data = data[-900:-1]

        х_deviation = []
        y_deviation = []
        z_deviation = []

        for i in minute_data:
            str(i)
            temp = i.split(' ')
            х_deviation.append(float(temp[-3]))
            y_deviation.append(float(temp[-2]))
            z_deviation.append(float(temp[-1]))

        x_difference = round(max(х_deviation) - min(х_deviation), 3)
        y_difference = round(max(y_deviation) - min(y_deviation), 3)
        z_difference = round(max(z_deviation) - min(z_deviation), 3)

        print(f'Разности: {x_difference}, {y_difference}, {z_difference}')

        q_degree = q_degree_return(x_difference, y_difference, z_difference)

        return q_degree

    except:
        print('Connection error')
        time.sleep(1)


# функция отправки результата анализа по базам данных
def analise_sender():

    logging.info('Функция анализа запущена')

    degree_for_sender = graphs_analise_now()
    q_degree_list = [1,2,3,4,5,6,7,8,9]

    for degree in q_degree_list:

        graphs_analise(degree, degree_for_sender)

    logging.info('Функция анализа завершена')


