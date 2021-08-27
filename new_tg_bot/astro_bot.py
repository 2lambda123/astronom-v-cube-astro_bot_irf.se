#!/usr/bin/python
# -*- coding: utf-8 -*-

from sending_schelude import job_sending
from longpool import job_longpool
from threading import Thread
import schedule
from functions.db_functions import *
from functions.sending_functions import *
from functions.analise_functions import *
import time

job_longpool()
