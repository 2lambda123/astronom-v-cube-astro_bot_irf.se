from keyboards import standart_keyboard
from functions.db_functions import *
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