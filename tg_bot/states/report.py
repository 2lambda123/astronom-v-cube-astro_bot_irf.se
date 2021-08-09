from aiogram import Dispatcher, types
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from secret_data import *

bot = Bot(token = main_token, parse_mode = types.ParseMode.HTML)

class BotReport(StatesGroup):
    report = State()

async def report_step_one(message: types.Message):

    await message.answer('Расскажите, в чем состоит проблема?', reply_markup = types.ReplyKeyboardRemove())
    await BotReport.report.set()


async def report_step_two(message: types.Message, state: FSMContext):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(emojize(":chart_with_upwards_trend: Графики :chart_with_upwards_trend:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass: Сейчас :hourglass:"))
    await bot.send_message(chat_id = 792302351, text = emojize(f":warning: Баг-репорт :warning:\nID пользователя: {message.from_user.id}\nТекст баг-репорта: {message.text}"))
    await message.answer('Ваш баг-репорт отправлен разработчику бота, в ближайшее время он займется исправлением неисправности. Спасибо :)', reply_markup = keyboard)

    await state.finish()


def register_handlers_report_command(dp: Dispatcher):
    dp.register_message_handler(report_step_one, commands = "bugreport", state = "*")
    dp.register_message_handler(report_step_two, state = BotReport.report)

def register_handlers_report_text(dp: Dispatcher):
    dp.register_message_handler(report_step_one, Text(equals = emojize(":warning: Баг-репорт :warning:")), state = "*")
    dp.register_message_handler(report_step_two, state = BotReport.report)
