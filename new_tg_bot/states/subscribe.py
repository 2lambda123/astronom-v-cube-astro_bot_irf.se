from aiogram import Dispatcher, types
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from secret_data import *
from functions.db_functions import *
import asyncio


bot = Bot(token = main_token, parse_mode = types.ParseMode.HTML)

class BotSubscriber(StatesGroup):
    subscriber = State()

def emojize_decryption(msg):

    if msg == emojize(":one:"):
        return (1)

    elif msg == emojize(":two:"):
        return (2)

    elif msg == emojize(":three:"):
        return (3)

    elif msg == emojize(":four:"):
        return (4)

    elif msg == emojize(":five:"):
        return (5)

    elif msg == emojize(":six:"):
        return (6)

    elif msg == emojize(":seven:"):
        return (7)

    elif msg == emojize(":eight:"):
        return (8)

    elif msg == emojize(":nine:"):
        return (9)


async def subscriber_step_one(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":one:"), emojize(":two:"), emojize(":three:")).add(emojize(":four:"), emojize(":five:"), emojize(":six:")).add(emojize(":seven:"), emojize(":eight:"), emojize(":nine:")).add(emojize(":arrow_up: В начало :arrow_up:"))
    await message.answer('Какой уровень Q вас интересует? (Узнать уровень Q для вашей широты можно, написав мне слово "Уровни")', reply_markup = keyboard)
    await BotSubscriber.subscriber.set()

async def subscriber_step_two(message: types.Message, state: FSMContext):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    degree = emojize_decryption(message.text)
    await insert_into_db(message.from_user.id, degree, keyboard)
    await state.finish()


def register_handlers_subscriber_commands(dp: Dispatcher):
    dp.register_message_handler(subscriber_step_one, commands = "subscribe",  state = "*")
    dp.register_message_handler(subscriber_step_two, state = BotSubscriber.subscriber)

def register_handlers_subscriber_text(dp: Dispatcher):
    dp.register_message_handler(subscriber_step_one, Text(equals = emojize(":bell: Подписаться :bell:")),  state = "*")
    dp.register_message_handler(subscriber_step_two, state = BotSubscriber.subscriber)
