#!/usr/bin/python
# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import urllib.request
import urllib3
import requests
import asyncio
import time
from secret_data import *
from astro_bot_vars import *
from states.report import *
from states.subscribe import *
from states.unsubscribe import *
from functions.db_functions import *
from functions.sending_functions import *
from functions.analise_functions import *

print('Диспетчер запущен...')


bot = Bot(token = main_token, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot, storage = MemoryStorage())

standart_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
standart_keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))

register_handlers_report_command(dp)
register_handlers_report_text(dp)
register_handlers_subscriber_commands(dp)
register_handlers_subscriber_text(dp)
register_handlers_unsubscriber_commands(dp)
register_handlers_unsubscriber_text(dp)

@dp.message_handler(commands = 'start')
@dp.message_handler(Text(equals = "Старт"))
@dp.message_handler(Text(equals = "старт"))
@dp.message_handler(Text(equals = "Начать"))
@dp.message_handler(Text(equals = "начать"))
@dp.message_handler(Text(equals = "Привет"))
@dp.message_handler(Text(equals = "привет"))
async def start(message: types.Message):
    await send(message.from_user.id, hello, standart_keyboard)

@dp.message_handler(commands = 'help')
@dp.message_handler(Text(equals = emojize(":memo: Команды :memo:")))
@dp.message_handler(Text(equals = "Команды"))
@dp.message_handler(Text(equals = "команды"))
async def help(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":bell: Подписаться :bell:")).add(emojize(":no_bell: Отписаться :no_bell:"), emojize(":x: Стоп :x:")).add(emojize(":bar_chart: Уровни Q :bar_chart:"), emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:")).add(emojize(":warning: Баг-репорт :warning:"), emojize(":arrow_up: В начало :arrow_up:"))
    await send(message.from_user.id, commands, keyboard)

@dp.message_handler(commands = 'q_degree')
@dp.message_handler(Text(equals = emojize(":bar_chart: Уровни Q :bar_chart:")))
@dp.message_handler(Text(equals = "Уровни"))
@dp.message_handler(Text(equals = "уровни"))
async def q_degree(message: types.Message):
    await send(message.from_user.id, degree_q, standart_keyboard)

@dp.message_handler(Text(equals = emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:")))
@dp.message_handler(Text(equals = "Графики"))
@dp.message_handler(Text(equals = "графики"))
async def graphs(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add("Primary", "Secondary (DMI)").add("K&Q index", "All graphs")
    await send(message.from_user.id, 'Какой график вас интересует?', keyboard)

@dp.message_handler(Text(equals = emojize(":arrow_up: В начало :arrow_up:")))
@dp.message_handler(Text(equals = "В начало"))
@dp.message_handler(Text(equals = "в начало"))
@dp.message_handler(commands = 'now')
@dp.message_handler(Text(equals = emojize(":hourglass: Сейчас :hourglass:")))
@dp.message_handler(Text(equals = "Сейчас"))
@dp.message_handler(Text(equals = "сейчас"))
async def graphs(message: types.Message):
    await send(message.from_user.id, f'Текущий уровень Q - {graphs_analise_now()}', standart_keyboard)

@dp.message_handler(commands = 'stop')
@dp.message_handler(Text(equals = emojize(":x: Стоп :x:")))
@dp.message_handler(Text(equals = "Стоп"))
@dp.message_handler(Text(equals = "стоп"))
async def stop(message: types.Message):
    await delete_from_db_for_id(message.from_user.id, standart_keyboard)

@dp.message_handler(Text(equals = "Primary"))
async def graphs_1(message: types.Message):
    img = urllib.request.urlopen(url_picture_1, timeout = 30).read()
    await send_attachment(message.from_user.id, img, standart_keyboard)

@dp.message_handler(Text(equals = "Secondary (DMI)"))
async def graphs_2(message: types.Message):
    img = urllib.request.urlopen(url_picture_2, timeout = 30).read()
    await send_attachment(message.from_user.id, img, standart_keyboard)

@dp.message_handler(Text(equals = "K&Q index"))
async def graphs_3(message: types.Message):
    img = urllib.request.urlopen(url_picture_3, timeout = 30).read()
    await send_attachment(message.from_user.id, img, standart_keyboard)

@dp.message_handler(Text(equals = "All graphs"))
async def graphs_all(message: types.Message):

    img_1 = urllib.request.urlopen(url_picture_1, timeout = 30).read()
    img_2 = urllib.request.urlopen(url_picture_2, timeout = 30).read()
    img_3 = urllib.request.urlopen(url_picture_3, timeout = 30).read()

    await send_attachment(message.from_user.id, img_1, standart_keyboard)
    await send_attachment(message.from_user.id, img_2, standart_keyboard)
    await send_attachment(message.from_user.id, img_3, standart_keyboard)

def job_longpull():
    executor.start_polling(dp)
