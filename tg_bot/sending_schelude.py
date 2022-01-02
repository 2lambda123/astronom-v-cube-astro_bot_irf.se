#!/usr/bin/python
# -*- coding: utf-8 -*-
import schedule
from functions.analise_functions import *
import time
from threading import Thread

logging.info('Рассылка запущена...')

schedule.every(1).minutes.do(analise_sender)

def job_sending():
    while True:
        schedule.run_pending()
        time.sleep(2)
