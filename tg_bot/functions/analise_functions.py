from PIL import Image
import urllib.request
import urllib3
import requests
from tqdm import tqdm
from functions.db_functions import *
from config import *
from astro_bot_vars import *


def sending(degree, degree_for_sender):

    list_id = search_into_db(degree)

    for id_one in list_id:

        bot.send_message(chat_id = id_one, text = emojize(f':red_exclamation_mark: Внимание! График достиг уровня {degree_for_sender} :red_exclamation_mark:'), reply_markup = standart_keyboard)

    print(f'Выполнил рассылку уровня {degree}')


# функция проверки графика и высылания ответа с анализом
def graphs_analise(degree, degree_for_sender):

    img = urllib.request.urlopen(url_picture_3, timeout = 30).read()
    out = open("K&Q index.png", "wb")
    out.write(img)
    out.close()

    image = Image.open("K&Q index.png") # Открываем изображение
    pix = image.load()            # Выгружаем значения пикселей

    x = 1185

    if degree == 1:
        y = 145
    elif degree == 2:
        y = 131
    elif degree == 3:
        y = 118
    elif degree == 4:
        y = 105
    elif degree == 5:
        y = 91
    elif degree == 6:
        y = 78
    elif degree == 7:
        y = 65
    elif degree == 8:
        y = 51
    elif degree == 9:
        y = 38

    color = str((pix[x, y]))
    sample_color = str((255, 255, 255))

    if color != sample_color:

        sending(degree, degree_for_sender)


# функция проверки графика в данный момент
def graphs_analise_now():

    img = urllib.request.urlopen(url_picture_3, timeout = 30).read()
    out = open("K&Q index.png", "wb")
    out.write(img)
    out.close()

    image = Image.open("K&Q index.png") # Открываем изображение
    pix = image.load()            # Выгружаем значения пикселей

    x = 1185
    y_1 = 145
    y_2 = 131
    y_3 = 118
    y_4 = 105
    y_5 = 91
    y_6 = 78
    y_7 = 65
    y_8 = 51
    y_9 = 38

    sample_color = str((255, 255, 255))

    if str((pix[x, y_9])) != sample_color:
        return 9
    elif str((pix[x, y_8])) != sample_color:
        return 8
    elif str((pix[x, y_7])) != sample_color:
        return 7
    elif str((pix[x, y_6])) != sample_color:
        return 6
    elif str((pix[x, y_5])) != sample_color:
        return 5
    elif str((pix[x, y_4])) != sample_color:
        return 4
    elif str((pix[x, y_3])) != sample_color:
        return 3
    elif str((pix[x, y_2])) != sample_color:
        return 2
    elif str((pix[x, y_1])) != sample_color:
        return 1
    else:
        return 0


# функция отправки результата анализа по базам данных
def analise_sender():
    print('Функция анализа запущена')

    degree_for_sender = graphs_analise_now()
    q_degree_list = [1,2,3,4,5,6,7,8,9]

    for degree in tqdm(q_degree_list, ncols = 175):

        graphs_analise(degree, degree_for_sender)

    print('Функция анализа завершена')
