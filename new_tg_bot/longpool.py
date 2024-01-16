import telebot
import urllib
from config import *
from bot_vars import *
from db_functions import *
from analise_functions import get_q_degree, q_degree
from keyboards import *

#############################################
# Параметры логгирования
import logging
logging.basicConfig(filename = 'logs.log',  filemode='a', level = logging.INFO, format = ' %(asctime)s - %(levelname)s - %(message)s', encoding = "UTF-8", datefmt='%d-%b-%y %H:%M:%S')

#############################################
# Создание объекта лонгпула и его запуск
bot = telebot.TeleBot(main_token)
logging.info('Start longpool...')

##########################################################################################
# Базовые функции - отправка сообщения и картинки + клавиатура
def send(user_id, msg, keyboard):
    logging.info(f'Send: "{msg}", id: {user_id}')
    return bot.send_message(user_id, msg, reply_markup = keyboard, parse_mode='html')

def send_attachment(user_id, image, keyboard):
    logging.info(f'Send photo, id: {user_id}')
    return bot.send_photo(user_id, image, reply_markup = keyboard)

##########################################################################################
# Функция рассылки
def sending(degree):
    if get_q_degree() != 0: 
        list_id = search_into_db(degree)
        for id_one in list_id:
            try:
                send(id_one, emojize(f':red_exclamation_mark:Значение q - {get_q_degree()}:red_exclamation_mark:'), standart_keyboard)

            except Exception as exception:
                logging.info(f'Problems with id: {id_one}')
                logging.error(f'Error: {exception}')
                delete_from_db(id_one)
                continue

    logging.info(f'Finish sending {get_q_degree()} degree')

##########################################################################################
# Ветка подписывания на уровень
@bot.message_handler(func = lambda message: message.text.lower() in ["/subscribe", "подписаться", emojize(":bell: подписаться :bell:")])
def subscribe(message):
    send(message.from_user.id, 'Какой уровень Q вас интересует? (Узнать уровень Q для вашей широты можно, написав мне слово "Уровни")', subscribe_keyboard)
    bot.register_next_step_handler(message, subscribe_get_degree)

def subscribe_get_degree(message):
    if message.text.lower() in [emojize(":bar_chart: уровни q :bar_chart:")]:
        send(message.chat.id, degree_q, standart_keyboard)

    elif message.text.lower() in [emojize(":counterclockwise_arrows_button: в начало :counterclockwise_arrows_button:")]:
        send(message.chat.id, f'Текущий уровень q - {get_q_degree()}', standart_keyboard)

    else:
        q_degree = emojize_decryption(message.text)
        
        try:
            try:
                delete_from_db(message.chat.id)
            except:
                pass
            insert_into_db(message.chat.id, q_degree)   
            logging.info(f"record ({message.chat.id}, {q_degree}) successfully inserted")
            send(message.chat.id, 'Вы добавлены в рассылку! Теперь вы будете получать уведомления, если график достигнет или превысит значение q, которое вы указали', standart_keyboard)  

        except (Exception, Error) as error:
            logging.info("error when working with PostgreSQL", error)
            send(message.chat.id, 'Произошла ошибка! Вероятно, вы уже подписаны на данный уровень q', standart_keyboard)

##########################################################################################
# Ветка отписывания
@bot.message_handler(func = lambda message: message.text.lower() in ["/unsubscribe", "отписаться", emojize(":bell_with_slash: отписаться :bell_with_slash:")])
def unsubscribe(message):
    try:
        delete_from_db(message.chat.id)
        logging.info(f'record about {message.chat.id} successfully removed')
        send(message.chat.id, 'Вы исключены из рассылки! Больше вы не будете получать уведомления', standart_keyboard)

    except (Exception, Error) as error:
        logging.info("error when working with PostgreSQL", error)
        send(message.chat.id, f'Произошла ошибка: {error}. Пожалуйста, сообщите о ней в баг-репорте', standart_keyboard)

##########################################################################################
# Получение багрепорта
@bot.message_handler(func = lambda message: message.text.lower() in ["/bugreport", "помощь", emojize(":warning: баг-репорт :warning:"), "багрепорт", "баг-репорт"])
def bugreport(message):

    send(message.from_user.id, 'Пожалуйста, опишите проблему', types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_bugreport)  # следующий шаг – функция get_bugreport

def get_bugreport(message):
    send(792302351, f'{emojize(":warning: Баг-репорт :warning:")}\nТекст баг-репорта: {message.text}\nОтправитель: {message.from_user.id}', None)
    send(message.chat.id, 'Ваш баг-репорт отправлен разработчику бота, в ближайшее время он займется исправлением неисправности. Спасибо :)', standart_keyboard)

##########################################################################################
# Ответ от админа на багрепорт
@bot.message_handler(func = lambda message: message.text.lower() in ["/admin"])
def admin_send(message):
    send(message.from_user.id, 'ID пользователя: ...', types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_send_id)  # следующий шаг – функция get_send_id

def get_send_id(message):
    global id
    id = message.text
    send(message.from_user.id, 'Текст сообщения для пользователя: ...', None)
    bot.register_next_step_handler(message, get_send_msg)  # следующий шаг – функция get_send_msg

def get_send_msg(message):
    text = message.text
    send(id, text, standart_keyboard)
    send(message.from_user.id, 'Сообщение отправлено', standart_keyboard)

##########################################################################################
# Основная ветка лонгпула
@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text.lower() in ['старт', 'начать', 'привет', '/start']:
        send(message.chat.id, hello, standart_keyboard)

    elif message.text.lower() in ['команды', '/help', emojize(":memo: команды :memo:")]:
        send(message.chat.id, commands, commands_keyboard)

    elif message.text.lower() in ['широты', 'уровни', emojize(":bar_chart: уровни q :bar_chart:"), '/q_degree', 'ку', 'q']:
        send(message.chat.id, degree_q, standart_keyboard)

    elif message.text.lower() in ['графики', emojize(":chart_increasing: графики :chart_increasing:", 'график')]:
        send(message.chat.id, 'Какой график вас интересует?', graphs_keyboard)

    elif message.text.lower() in ['/now', 'в начало', 'сейчас', emojize(":counterclockwise_arrows_button: в начало :counterclockwise_arrows_button:"), emojize(":hourglass_not_done: сейчас :hourglass_not_done:")]:
        send(message.chat.id, f'Текущий уровень Q - {get_q_degree()}', standart_keyboard)

    elif message.text.lower() in ['/stop', 'стоп', emojize(":cross_mark: стоп :cross_mark:")]:
        delete_from_db(message.chat.id, False)

    elif message.text.lower() == 'primary':
        img = urllib.request.urlopen(url_picture_1, timeout=30).read()
        send_attachment(message.chat.id, img, standart_keyboard)

    elif message.text.lower() == 'secondary (dmi)':
        img = urllib.request.urlopen(url_picture_2, timeout=30).read()
        send_attachment(message.chat.id, img, standart_keyboard)

    elif message.text.lower() == 'k&q index':
        img = urllib.request.urlopen(url_picture_3, timeout=30).read()
        send_attachment(message.chat.id, img, standart_keyboard)

    elif message.text.lower() == 'all graphs':
        img_1 = urllib.request.urlopen(url_picture_1, timeout=30).read()
        send_attachment(message.from_user.id, img_1, standart_keyboard)
        img_2 = urllib.request.urlopen(url_picture_2, timeout=30).read()
        send_attachment(message.from_user.id, img_2, standart_keyboard)
        img_3 = urllib.request.urlopen(url_picture_3, timeout=30).read()
        send_attachment(message.from_user.id, img_3, standart_keyboard)

##########################################################################################
# Запуск лонгпула
def job_longpool():
    bot.infinity_polling()

##########################################################################################
