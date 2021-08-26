#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Process
from dispatcher import *
from sending_schelude import *
from threading import Thread
import schedule
from functions.db_functions import *
from functions.sending_functions import *
from functions.analise_functions import *
import time

p1 = Process(target = job_longpull)
p2 = Process(target = job_sending)

def work_process():
    p1.start()
    p2.start()

    p1.join()
    p2.join()

if __name__ == "__main__":
    work_process()
