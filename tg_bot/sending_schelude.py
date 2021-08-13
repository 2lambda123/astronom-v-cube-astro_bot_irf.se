#!/usr/bin/python
# -*- coding: utf-8 -*-
import schedule
from functions.analise_functions import *
import time
from threading import Thread

print('Рассылка запущена...')

schedule.every().hour.at(":01").do(analise_sender)
schedule.every().hour.at(":16").do(analise_sender)
schedule.every().hour.at(":31").do(analise_sender)
schedule.every().hour.at(":46").do(analise_sender)

def job_sending():
    while True:
        schedule.run_pending()
        time.sleep(30)
