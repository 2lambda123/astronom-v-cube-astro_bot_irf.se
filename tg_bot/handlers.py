from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import urllib.request
from secret_data import *
from astro_bot_vars import *

bot = Bot(token = main_token, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot, storage = MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

def send(user_id, msg, keyboard):

    print(f'Ответил: "{msg}" пользователю с id: {user_id}')
    return bot.send_message(chat_id = user_id, text = msg, reply_markup = keyboard)

def send_attachment(user_id, image, keyboard):

    print(f'Ответил: фото пользователю с id: {user_id}')
    return bot.send_photo(chat_id = user_id, photo = image, reply_markup = keyboard)

@dp.message_handler(commands = 'start')
@dp.message_handler(Text(equals = "Старт"))
@dp.message_handler(Text(equals = "старт"))
@dp.message_handler(Text(equals = "Начать"))
@dp.message_handler(Text(equals = "начать"))
@dp.message_handler(Text(equals = "Привет"))
@dp.message_handler(Text(equals = "привет"))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await send(message.from_user.id, hello, keyboard)

@dp.message_handler(commands = 'help')
@dp.message_handler(Text(equals = emojize(":memo: Команды :memo:")))
@dp.message_handler(Text(equals = "Команды"))
@dp.message_handler(Text(equals = "команды"))
async def help(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":bell: Подписаться :bell:"), emojize(":no_bell: Отписаться :no_bell:"), emojize(":x: Стоп :x:")).add(emojize(":bar_chart: Уровни Q :bar_chart:"), emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:")).add(emojize(":warning: Баг-репорт :warning:"), emojize(":arrow_up: В начало :arrow_up:"))
    await send(message.from_user.id, commands, keyboard)

@dp.message_handler(commands = 'q_degree')
@dp.message_handler(Text(equals = emojize(":bar_chart: Уровни Q :bar_chart:")))
@dp.message_handler(Text(equals = "Уровни"))
@dp.message_handler(Text(equals = "уровни"))
async def q_degree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await send(message.from_user.id, degree_q, keyboard)

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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await send(message.from_user.id, f'Текущий уровень Q - ', keyboard)

@dp.message_handler(commands = 'stop')
@dp.message_handler(Text(equals = emojize(":x: Стоп :x:")))
@dp.message_handler(Text(equals = "Стоп"))
@dp.message_handler(Text(equals = "стоп"))
async def stop(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await message.answer('Отписываю!!!!!!!!!!!!!!!!', reply_markup = keyboard)

@dp.message_handler(Text(equals = "Primary"))
async def graphs_1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    img = urllib.request.urlopen(url_picture_1, timeout = 30).read()
    await send_attachment(message.from_user.id, img, keyboard)

@dp.message_handler(Text(equals = "Secondary (DMI)"))
async def graphs_2(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    img = urllib.request.urlopen(url_picture_2, timeout = 30).read()
    await send_attachment(message.from_user.id, img, keyboard)

@dp.message_handler(Text(equals = "K&Q index"))
async def graphs_3(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    img = urllib.request.urlopen(url_picture_3, timeout = 30).read()
    await send_attachment(message.from_user.id, img, keyboard)

@dp.message_handler(Text(equals = "All graphs"))
async def graphs_all(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))

    img_1 = urllib.request.urlopen(url_picture_1, timeout = 30).read()
    img_2 = urllib.request.urlopen(url_picture_2, timeout = 30).read()
    img_3 = urllib.request.urlopen(url_picture_3, timeout = 30).read()

    await send_attachment(message.from_user.id, img_1, keyboard)
    await send_attachment(message.from_user.id, img_2, keyboard)
    await send_attachment(message.from_user.id, img_3, keyboard)
