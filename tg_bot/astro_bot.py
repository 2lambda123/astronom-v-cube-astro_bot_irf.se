#!/usr/bin/python
# -*- coding: utf-8 -*-
import vk_api
import time
import schedule
import psycopg2
from psycopg2 import Error
from threading import Thread
from PIL import Image
import urllib.request
import urllib3
import requests
import socket
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from secret_data import *
from astro_bot_vars import *

socket.setdefaulttimeout(60)

print ('Бот запущен...')


# # функция добавления пользователя в рассылку
# def insert_into_db(id, q_degree, keyboard):
#     try:
#         # Подключение к существующей базе данных
#         connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)
#
#         # Курсор для выполнения операций с базой данных
#         cursor = connection.cursor()
#
#         # Выполнение SQL-запроса для вставки данных в таблицу
#         insert_query = f" INSERT INTO users VALUES ({id}, {q_degree}) "
#         cursor.execute(insert_query)
#         connection.commit()
#         print("Запись успешно вставлена")
#         vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы добавлены в рассылку! Теперь вы будете получать уведомления, если график достигнет или превысит значение Q, которое вы указали')
#
#     except (Exception, Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#         vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка! Вероятно, вы уже подписаны на данный уровень Q')
#
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             print("Соединение с PostgreSQL закрыто")
#
#
# # функция удаления пользователя из базы данных
# def delete_from_db(id, q_degree, keyboard):
#     try:
#         # Подключение к существующей базе данных
#         connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)
#
#         # Курсор для выполнения операций с базой данных
#         cursor = connection.cursor()
#
#         # Выполнение SQL-запроса для удаления значения из таблицы
#         delete_query = f" DELETE FROM users WHERE id = {id} AND q_degree = {q_degree} "
#         cursor.execute(delete_query)
#         connection.commit()
#         print("Запись успешно удалена")
#         vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы исключены из рассылки! Больше вы не будете получать уведомления об этом уровне Q')
#
#     except (Exception, Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#         vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка! Вероятно, вы не подписаны на данный уровень Q')
#
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             print("Соединение с PostgreSQL закрыто")
#
#
# # функция отключения пользователя от базы данных
# def delete_from_db_for_id(id, keyboard):
#     try:
#         # Подключение к существующей базе данных
#         connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)
#
#         # Курсор для выполнения операций с базой данных
#         cursor = connection.cursor()
#
#         # Выполнение SQL-запроса для удаления значения из таблицы
#         delete_query = f" DELETE FROM users WHERE id = {id} "
#         cursor.execute(delete_query)
#         connection.commit()
#         print("Запись успешно удалена")
#         vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы исключены из рассылки! Больше вы не будете получать уведомления')
#
#     except (Exception, Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#         vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка!')
#
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             print("Соединение с PostgreSQL закрыто")
#
#
# # функция поиска пользователей по базе данных и создания списка рассылки
# def search_into_db(q_degree):
#     try:
#         # Подключение к существующей базе данных
#         connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)
#
#         # Курсор для выполнения операций с базой данных
#         cursor = connection.cursor()
#
#         # Выполнение SQL-запроса для поиска данных в таблице
#         insert_query = f" SELECT id FROM USERS WHERE q_degree = {q_degree} "
#         cursor.execute(insert_query)
#         rows = cursor.fetchall()
#
#         list_id = []
#
#         for row in rows:
#             list_id.append(row[0])
#
#         return(list_id)
#
#     except (Exception, Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             print("Соединение с PostgreSQL закрыто")
#
# функция отправки текстового сообщения
def send(event, msg, kbd):

    if event.obj['peer_id'] > 2e9:       #если чат
        print(f'Ответил: "{msg}" для беседы с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], message = msg)
    else:
        print(f'Ответил: "{msg}" для пользователя с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], keyboard = kbd.get_keyboard(), message = msg)


# функция отправки сообщения с фото
def send_attachment(event, image, kbd):

    if event.obj['peer_id'] > 2e9:       #если чат
        print(f'Отправил фото для беседы с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], attachment = image)
    else:
        print(f'Отправил фото для пользователя с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], keyboard = kbd.get_keyboard(), attachment = image)


# функция рассылки оповещения
def sending(degree, degree_for_sender):

    list_id = search_into_db(degree)

    for id_one in list_id:
        vk.messages.send(random_id = get_random_id(), peer_id = id_one, keyboard = keyboard.get_keyboard(), message = f'&#10071;Внимание! График достиг уровня {degree_for_sender}&#10071;')

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
    graphs_analise(1, degree_for_sender)
    graphs_analise(2, degree_for_sender)
    graphs_analise(3, degree_for_sender)
    graphs_analise(4, degree_for_sender)
    graphs_analise(5, degree_for_sender)
    graphs_analise(6, degree_for_sender)
    graphs_analise(7, degree_for_sender)
    graphs_analise(8, degree_for_sender)
    graphs_analise(9, degree_for_sender)

    print('Функция анализа завершена')


th_1 = Thread(target = job_longpool)

def run_threaded(job_func):
    job_thread = Thread(target = job_func)
    job_thread.start()

schedule.every().hour.at(":01").do(run_threaded, analise_sender)
schedule.every().hour.at(":16").do(run_threaded, analise_sender)
schedule.every().hour.at(":31").do(run_threaded, analise_sender)
schedule.every().hour.at(":46").do(run_threaded, analise_sender)

# функция запуска многопоточной работы бота
if __name__ == '__main__':

    th_1.start()
    while True:
        schedule.run_pending()
        time.sleep(30)
