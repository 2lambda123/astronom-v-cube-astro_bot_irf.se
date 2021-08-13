from aiogram import Bot, types
from secret_data import *

bot = Bot(token = main_token, parse_mode = types.ParseMode.HTML)

def send(user_id, msg, keyboard):

    print(f'Ответил: "{msg}" пользователю с id: {user_id}')
    return bot.send_message(chat_id = user_id, text = msg, reply_markup = keyboard)

def send_attachment(user_id, image, keyboard):

    print(f'Ответил фото пользователю с id: {user_id}')
    return bot.send_photo(chat_id = user_id, photo = image, reply_markup = keyboard)

def sending(degree, degree_for_sender):

    list_id = search_into_db(degree)

    for id_one in list_id:

        bot.send_message(chat_id = id_one, text = emojize(f':heavy_exclamation_mark: Внимание! График достиг уровня {degree_for_sender} :heavy_exclamation_mark:'), reply_markup = standart_keyboard)

    print(f'Выполнил рассылку уровня {degree}')
