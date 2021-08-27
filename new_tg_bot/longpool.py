from secret_data import *
from astro_bot_vars import *
from functions.db_functions import *
from functions.sending_functions import *
from functions.analise_functions import *
import telebot
import urllib
from keyboards import *

print('Бот запущен...')

bot = telebot.TeleBot(main_token)

@bot.message_handler(func = lambda message: message.text.lower() == "/subscribe")
@bot.message_handler(func = lambda message: message.text.lower() == "подписаться")
@bot.message_handler(func = lambda message: message.text.lower() == ":bell: подписаться :bell:")
def subscribe(message):

    send(message.from_user.id, 'Какой уровень Q вас интересует? (Узнать уровень Q для вашей широты можно, написав мне слово "Уровни")', subscribe_keyboard)

    bot.register_next_step_handler(message, get_degree); #следующий шаг – функция get_name


def get_degree(message):

    q_degree = emojize_decryption(message.text)

    insert_into_db(message.from_user.id, q_degree)



@bot.message_handler(content_types = ["text"])

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

        img = urllib.request.urlopen(url_picture_1, timeout = 30).read()
        send_attachment(message.chat.id, img, standart_keyboard)

    elif message.text.lower() == 'secondary (dmi)':

        img = urllib.request.urlopen(url_picture_2, timeout = 30).read()
        send_attachment(message.chat.id, img, standart_keyboard)

    elif message.text.lower() == 'k&q index':

        img = urllib.request.urlopen(url_picture_3, timeout = 30).read()
        send_attachment(message.chat.id, img, standart_keyboard)

    elif message.text.lower() == 'all graphs':

        img_1 = urllib.request.urlopen(url_picture_1, timeout = 30).read()
        send_attachment(message.from_user.id, img_1, standart_keyboard)
        img_2 = urllib.request.urlopen(url_picture_2, timeout = 30).read()
        send_attachment(message.from_user.id, img_2, standart_keyboard)
        img_3 = urllib.request.urlopen(url_picture_3, timeout = 30).read()
        send_attachment(message.from_user.id, img_3, standart_keyboard)

def job_longpool():

    bot.infinity_polling()
