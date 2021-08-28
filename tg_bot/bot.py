#!/usr/bin/python
# -*- coding: utf-8 -*-

from sending_schelude import job_sending
from longpool import job_longpool
from threading import Thread

print('Бот запущен...')

th_1 = Thread(target = job_longpool)
th_2 = Thread(target = job_sending)

# функция запуска многопоточной работы бота
if __name__ == '__main__':

    th_1.start()
    th_2.start()
