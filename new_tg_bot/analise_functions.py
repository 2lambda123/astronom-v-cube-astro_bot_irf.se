from bot_vars import *
import logging
import time
import urllib3

logging.basicConfig(filename = 'logs.log',  filemode='w', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', datefmt = '%d-%b-%y %H:%M:%S', encoding = "UTF-8")

#############################################
# Получение максимальных разностей за 15 минут (900) записей и определение уровня q
def get_q_degree():

    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url_text, headers={'Range':'bytes=-35000'})
        q_data = response.data.decode("utf-8").splitlines()[-901:-1]

        х_deviation = []
        y_deviation = []
        z_deviation = []

        for i in q_data:
            str(i)
            temp = i.split(' ')
            х_deviation.append(float(temp[-3]))
            y_deviation.append(float(temp[-2]))
            z_deviation.append(float(temp[-1]))

        x_difference = round(max(х_deviation) - min(х_deviation), 3)
        y_difference = round(max(y_deviation) - min(y_deviation), 3)
        z_difference = round(max(z_deviation) - min(z_deviation), 3)

        logging.info(f'difference: {x_difference}, {y_difference}, {z_difference}')

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
        
    except:
        logging.info(f'Connection error. Connecting...')
        time.sleep(1)

#############################################

q_degree = get_q_degree()