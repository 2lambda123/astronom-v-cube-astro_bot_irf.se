#!/usr/bin/python
# -*- coding: utf-8 -*-

from longpool import job_longpool
from threading import Thread
import logging
import schedule
from analise_functions import get_q_degree
from longpool import sending
import time

def analise_sender():

    logging.info('Start analysis and sending...')

    q_degree_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for degree in q_degree_list:
        sending(degree)

    logging.info('Finish analysis and sending')

schedule.every(1).minutes.do(analise_sender)

def job_sending():
    while True:
        schedule.run_pending()
        time.sleep(2)

##########################################################################################

logging.basicConfig(filename = 'logs.log',  filemode='a', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', encoding = "UTF-8", datefmt='%d-%b-%y %H:%M:%S')

logging.info('Start bot...')

th_1 = Thread(target = job_longpool)
th_2 = Thread(target = job_sending)

##########################################################################################
# функция запуска многопоточной работы бота
if __name__ == '__main__':

    th_1.start()
    th_2.start()



