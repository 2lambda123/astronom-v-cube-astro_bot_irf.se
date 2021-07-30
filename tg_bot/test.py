from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from secret_data import *
from astro_bot_vars import *
from state_machine import States

print('Бот запущен')

class Subscriptions(Helper):
    subscriber = State()
    unsubscriber = State()
    report = State()

bot = Bot(token = main_token, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot, storage = MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

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
    await message.answer(hello, reply_markup = keyboard)

@dp.message_handler(commands = 'help')
@dp.message_handler(Text(equals = emojize(":memo: Команды :memo:")))
@dp.message_handler(Text(equals = "Команды"))
@dp.message_handler(Text(equals = "команды"))
async def help(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":bell: Подписаться :bell:"), emojize(":no_bell: Отписаться :no_bell:"), emojize(":x: Стоп :x:")).add(emojize(":bar_chart: Уровни Q :bar_chart:"), emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:")).add(emojize(":warning: Баг-репорт :warning:"), emojize(":arrow_up: В начало :arrow_up:"))
    await message.answer(commands, reply_markup = keyboard)

@dp.message_handler(commands = 'q_degree')
@dp.message_handler(Text(equals = emojize(":bar_chart: Уровни Q :bar_chart:")))
@dp.message_handler(Text(equals = "Уровни"))
@dp.message_handler(Text(equals = "уровни"))
async def q_degree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":one:"), emojize(":two:"), emojize(":three:")).add(emojize(":four:"), emojize(":five:"), emojize(":six:")).add(emojize(":seven:"), emojize(":eight:"), emojize(":nine:")).add(emojize(":arrow_up: В начало :arrow_up:"))
    await message.answer(degree_q, reply_markup = keyboard)

@dp.message_handler(Text(equals = emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:")))
@dp.message_handler(Text(equals = "Графики"))
@dp.message_handler(Text(equals = "графики"))
async def graphs(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add("Primary","Secondary (DMI)").add("K&Q index","All graphs")
    await message.answer('Какой график вас интересует?', reply_markup = keyboard)


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
    await message.answer(f'Присылаю текущий уровень ку!!!!!!!!!!', reply_markup = keyboard)

@dp.message_handler(commands = 'subscribe')
@dp.message_handler(Text(equals = emojize(":bell: Подписаться :bell:")))
@dp.message_handler(Text(equals = "Подписаться"))
@dp.message_handler(Text(equals = "подписаться"))
async def subscribe(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":one:"), emojize(":two:"), emojize(":three:")).add(emojize(":four:"), emojize(":five:"), emojize(":six:")).add(emojize(":seven:"), emojize(":eight:"), emojize(":nine:")).add(emojize(":arrow_up: В начало :arrow_up:"))
    await message.answer('Какой уровень Q вас интересует?', reply_markup = keyboard)
    await Subscriptions.subscribe()

@dp.message_handler(commands = 'unsubscribe')
@dp.message_handler(Text(equals = emojize(":no_bell: Отписаться :no_bell:")))
@dp.message_handler(Text(equals = "Отписаться"))
@dp.message_handler(Text(equals = "отписаться"))
async def unsubscribe(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize("Про :one:"), emojize("Про :two:"), emojize("Про :three:")).add(emojize("Про :four:"), emojize("Про :five:"), emojize("Про :six:")).add(emojize("Про :seven:"), emojize("Про :eight:"), emojize("Про :nine:")).add(emojize(":arrow_up: В начало :arrow_up:"))
    await message.answer('Про какой уровень Q вам больше не интересно получать информацию?', reply_markup = keyboard)

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
    await message.answer('Высылаю Праймари!!!!!!!!!!!!!!', reply_markup = keyboard)

@dp.message_handler(Text(equals = "Secondary (DMI)"))
async def graphs_2(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await message.answer('Высылаю секондари!!!!!!!!!!!!!!', reply_markup = keyboard)

@dp.message_handler(Text(equals = "K&Q index"))
async def graphs_3(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await message.answer('Высылаю индекс!!!!!!!!!!!!!!', reply_markup = keyboard)

@dp.message_handler(Text(equals = "All graphs"))
async def graphs_all(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await message.answer('Высылаю все!!!!!!!!!!!!!!', reply_markup = keyboard)

@dp.message_handler(Text(equals = "Багрепорт"))
async def start(message: types.Message, state: report):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await bot.send_message(chat_id = 792302351, text="Тестовая рассылка")
    await message.answer('Ваш баг-репорт отправлен разработчику бота, в ближайшее время он займется исправлением неисправности. Спасибо :)', reply_markup = keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
