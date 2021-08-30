from config import *
from bot_vars import *
from functions.db_functions import *
from functions.sending_functions import *
from functions.analise_functions import *
import telebot
import urllib
from keyboards import *
import logging

logging.basicConfig(filename = 'logs.log',  filemode='w', level = logging.INFO, format = ' %(asctime)s - %(levelname)s - %(message)s', encoding = "UTF-8", datefmt='%d-%b-%y %H:%M:%S', )

bot = telebot.TeleBot(main_token)

logging.info('Лонгпул запущен...')

@bot.message_handler(func = lambda message: message.text.lower() in ["/subscribe", "подписаться", emojize(":bell: подписаться :bell:")])

def subscribe(message):

    send(message.from_user.id, 'Какой уровень Q вас интересует? (Узнать уровень Q для вашей широты можно, написав мне слово "Уровни")', subscribe_keyboard)

    bot.register_next_step_handler(message, subscribe_get_degree)  # следующий шаг – функция get_name

def subscribe_get_degree(message):

    if message.text.lower() in [emojize(":bar_chart: уровни q :bar_chart:")]:
        send(message.chat.id, degree_q, standart_keyboard)

    elif message.text.lower() in [emojize(":counterclockwise_arrows_button: в начало :counterclockwise_arrows_button:")]:

        send(message.chat.id, f'Текущий уровень Q - {graphs_analise_now()}', standart_keyboard)

    else:

        q_degree = emojize_decryption(message.text)
        insert_into_db(message.from_user.id, q_degree)


@bot.message_handler(func = lambda message: message.text.lower() in ["/unsubscribe", "отписаться", emojize(":bell_with_slash: отписаться :bell_with_slash:")])

def unsubscribe(message):

    send(message.from_user.id, 'Про какой уровень Q вам больше не интересно получать информацию? (Узнать уровень Q для вашей широты можно, написав мне слово "Уровни")', subscribe_keyboard)

    bot.register_next_step_handler(message, unsubscribe_get_degree)  # следующий шаг – функция get_name

def unsubscribe_get_degree(message):

    if message.text.lower() in [emojize(":counterclockwise_arrows_button: в начало :counterclockwise_arrows_button:")]:

        send(message.chat.id, f'Текущий уровень Q - {graphs_analise_now()}', standart_keyboard)

    else:

        q_degree = emojize_decryption(message.text)
        delete_from_db(message.from_user.id, q_degree)


@bot.message_handler(func = lambda message: message.text.lower() in ["/bugreport", "помощь", emojize(":warning: баг-репорт :warning:"), "багрепорт", "баг-репорт"])

def bugreport(message):

    send(message.from_user.id, 'Пожалуйста, опишите проблему', types.ReplyKeyboardRemove())

    bot.register_next_step_handler(message, get_bugreport)  # следующий шаг – функция get_name

def get_bugreport(message):

    send(792302351, f'{emojize(":warning: Баг-репорт :warning:")}\nТекст баг-репорта: {message.text}\nОтправитель: {message.from_user.id}', None)
    send(message.chat.id, 'Ваш баг-репорт отправлен разработчику бота, в ближайшее время он займется исправлением неисправности. Спасибо :)', standart_keyboard)


@bot.message_handler(func = lambda message: message.text.lower() in ["/admin"])

def admin_send(message):

    send(message.from_user.id, 'ID пользователя: ...', types.ReplyKeyboardRemove())

    bot.register_next_step_handler(message, get_send_id)  # следующий шаг – функция get_name

def get_send_id(message):

    global id
    id = message.text

    send(message.from_user.id, 'Текст сообщения для пользователя: ...', None)

    bot.register_next_step_handler(message, get_send_msg)  # следующий шаг – функция get_name


def get_send_msg(message):

    text = message.text

    send(id, text, standart_keyboard)
    send(message.from_user.id, 'Сообщение отправлено', standart_keyboard)


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

        send(message.chat.id, f'Текущий уровень Q - {graphs_analise_now()}', standart_keyboard)

    elif message.text.lower() in ['/stop', 'стоп', emojize(":cross_mark: стоп :cross_mark:")]:

        delete_from_db_for_id(message.chat.id)

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


def job_longpool():
    bot.infinity_polling()
