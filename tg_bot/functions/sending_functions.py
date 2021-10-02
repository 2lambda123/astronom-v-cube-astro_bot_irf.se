from functions.db_functions import *
from keyboards import standart_keyboard
from config import *
import telebot
import logging

bot = telebot.TeleBot(main_token)

def send(user_id, msg, keyboard):

    logging.info(f'Ответил: "{msg}" пользователю с id: {user_id}')
    return bot.send_message(user_id, msg, reply_markup = keyboard, parse_mode='html')

def send_attachment(user_id, image, keyboard):

    logging.info(f'Отправил фото пользователю с id: {user_id}')
    return bot.send_photo(user_id, image, reply_markup = keyboard)

def sending(degree, degree_for_sender):

    list_id = search_into_db(degree)

    for id_one in list_id:

        bot.send_message(id_one, emojize(f':red_exclamation_mark:Внимание! График достиг уровня {degree_for_sender}:red_exclamation_mark:'), reply_markup = standart_keyboard)

    logging.info(f'Выполнил рассылку уровня {degree}')
