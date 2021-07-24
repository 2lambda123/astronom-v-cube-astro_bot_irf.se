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

keyboard = VkKeyboard(one_time = True)

keyboard.add_button('Графики', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Команды', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()  # Переход на вторую строку
keyboard.add_button('Сейчас', color=VkKeyboardColor.PRIMARY)

keyboard_two = VkKeyboard()

keyboard_two.add_button('Подписаться', color=VkKeyboardColor.POSITIVE)
keyboard_two.add_button('Отписаться', color=VkKeyboardColor.SECONDARY)
keyboard_two.add_button('Стоп', color=VkKeyboardColor.NEGATIVE)
keyboard_two.add_line()  # Переход на вторую строку
keyboard_two.add_button('Уровни Q', color=VkKeyboardColor.PRIMARY)
keyboard_two.add_button('Графики', color=VkKeyboardColor.PRIMARY)
keyboard_two.add_line()  # Переход на вторую строку
keyboard_two.add_button('Баг-репорт', color=VkKeyboardColor.NEGATIVE)
keyboard_two.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_three = VkKeyboard()

keyboard_three.add_button('Primary', color=VkKeyboardColor.SECONDARY)
keyboard_three.add_button('Secondary (DMI)', color=VkKeyboardColor.POSITIVE)
keyboard_three.add_line()  # Переход на вторую строку
keyboard_three.add_button('K&Q index', color=VkKeyboardColor.NEGATIVE)
keyboard_three.add_button('All graphs', color=VkKeyboardColor.PRIMARY)
keyboard_three.add_line()  # Переход на вторую строку
keyboard_three.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_four = VkKeyboard()

keyboard_four.add_button('1', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_button('2', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_button('3', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_line()  # Переход на вторую строку
keyboard_four.add_button('4', color=VkKeyboardColor.POSITIVE)
keyboard_four.add_button('5', color=VkKeyboardColor.POSITIVE)
keyboard_four.add_button('6', color=VkKeyboardColor.POSITIVE)
keyboard_four.add_line()  # Переход на вторую строку
keyboard_four.add_button('7', color=VkKeyboardColor.PRIMARY)
keyboard_four.add_button('8', color=VkKeyboardColor.PRIMARY)
keyboard_four.add_button('9', color=VkKeyboardColor.PRIMARY)
keyboard_four.add_line()  # Переход на вторую строку
keyboard_four.add_button('Уровни Q', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_five = VkKeyboard()

keyboard_five.add_button('Про 1', color=VkKeyboardColor.SECONDARY)
keyboard_five.add_button('Про 2', color=VkKeyboardColor.SECONDARY)
keyboard_five.add_button('Про 3', color=VkKeyboardColor.SECONDARY)
keyboard_five.add_line()  # Переход на вторую строку
keyboard_five.add_button('Про 4', color=VkKeyboardColor.POSITIVE)
keyboard_five.add_button('Про 5', color=VkKeyboardColor.POSITIVE)
keyboard_five.add_button('Про 6', color=VkKeyboardColor.POSITIVE)
keyboard_five.add_line()  # Переход на вторую строку
keyboard_five.add_button('Про 7', color=VkKeyboardColor.PRIMARY)
keyboard_five.add_button('Про 8', color=VkKeyboardColor.PRIMARY)
keyboard_five.add_button('Про 9', color=VkKeyboardColor.PRIMARY)
keyboard_five.add_line()  # Переход на вторую строку
keyboard_five.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_six = VkKeyboard()

keyboard_six.add_button('1', color=VkKeyboardColor.SECONDARY)
keyboard_six.add_button('2', color=VkKeyboardColor.SECONDARY)
keyboard_six.add_button('3', color=VkKeyboardColor.SECONDARY)
keyboard_six.add_line()  # Переход на вторую строку
keyboard_six.add_button('4', color=VkKeyboardColor.POSITIVE)
keyboard_six.add_button('5', color=VkKeyboardColor.POSITIVE)
keyboard_six.add_button('6', color=VkKeyboardColor.POSITIVE)
keyboard_six.add_line()  # Переход на вторую строку
keyboard_six.add_button('7', color=VkKeyboardColor.PRIMARY)
keyboard_six.add_button('8', color=VkKeyboardColor.PRIMARY)
keyboard_six.add_button('9', color=VkKeyboardColor.PRIMARY)
keyboard_six.add_line()  # Переход на вторую строку
keyboard_six.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

vk_session = VkApi(token = main_token)
vk = vk_session.get_api()


# функция добавления пользователя в рассылку
def insert_into_db(id, q_degree, keyboard):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f" INSERT INTO users VALUES ({id}, {q_degree}) "
        cursor.execute(insert_query)
        connection.commit()
        print("Запись успешно вставлена")
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы добавлены в рассылку! Теперь вы будете получать уведомления, если график достигнет или превысит значение Q, которое вы указали')

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка! Вероятно, вы уже подписаны на данный уровень Q')

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция удаления пользователя из базы данных
def delete_from_db(id, q_degree, keyboard):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для удаления значения из таблицы
        delete_query = f" DELETE FROM users WHERE id = {id} AND q_degree = {q_degree} "
        cursor.execute(delete_query)
        connection.commit()
        print("Запись успешно удалена")
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы исключены из рассылки! Больше вы не будете получать уведомления об этом уровне Q')

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка! Вероятно, вы не подписаны на данный уровень Q')

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция отключения пользователя от базы данных
def delete_from_db_for_id(id, keyboard):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для удаления значения из таблицы
        delete_query = f" DELETE FROM users WHERE id = {id} "
        cursor.execute(delete_query)
        connection.commit()
        print("Запись успешно удалена")
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы исключены из рассылки! Больше вы не будете получать уведомления')

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка!')

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция поиска пользователей по базе данных и создания списка рассылки
def search_into_db(q_degree):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для поиска данных в таблице
        insert_query = f" SELECT id FROM USERS WHERE q_degree = {q_degree} "
        cursor.execute(insert_query)
        rows = cursor.fetchall()

        list_id = []

        for row in rows:
            list_id.append(row[0])

        return(list_id)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

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

# функция прослушивания longpoll и ответа на ключевые слова
def job_longpool():
    print('Функция прослушивания longpool запущена')
    longpoll = VkBotLongPoll(vk_session, '202712381')
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    print('-' * 30)
                    print(f'Сообщение получено от id: ' + str({event.obj["peer_id"]}) )
                    print('-' * 30)
                    print('Текст сообщения: ' + str(event.object['text']))
                    print('-' * 30)

                    msg = event.object['text'].lower()
                    id = event.obj["peer_id"]

                    if msg in ('начать', 'привет', 'старт'):
                        send (event, hello, keyboard)

                    elif msg in ('test', 'тест'):
                        send (event, 'Бот работает успешно!', keyboard)

                    elif msg in ('команды', 'commands'):
                        send (event, commands, keyboard_two)

                    elif msg in ('сейчас', 'now'):
                        number = graphs_analise_now()
                        send (event, f"Текущий уровень Q - {number}", keyboard)

                    elif msg in ('в начало'):
                        number = graphs_analise_now()
                        send (event, f"Текущий уровень Q - {number}", keyboard)

                    elif msg in ('багрепорт', 'баг-репорт', 'баг'):
                        send (event, 'Если с ботом возникли какие-то проблемы, вы можете сообщить о них разработчику. Для этого напишите в одном сообщении: сначала слово "помощь", а затем опишите неполадку. Ваше сообщение будет отправлено разработчику бота', keyboard)

                    elif 'помощь' in msg or 'help' in msg:
                        vk.messages.send(random_id = get_random_id(), peer_id = 557660245, message = (f'&#10071;БАГ-РЕПОРТ&#10071; {event}'))
                        send (event, 'Ваш баг-репорт отправлен разработчику бота, в ближайшее время он займется исправлением неисправности. Спасибо :)', keyboard)

                    elif msg in ('уровни', 'уровни q', 'уровень', 'уровень q', 'q'):
                        send (event, degree_Q, keyboard_six)

                    elif msg in ('график', 'графики'):
                        send (event, "Какой график вас интересует?", keyboard_three)

                    elif msg in ('рассылка', 'подписка', 'подписка на рассылку', 'подписаться'):
                        send (event, 'Какой уровень Q вас интересует? (Узнать уровень Q для вашей широты можно, написав мне слово "Уровни")', keyboard_four)

                    elif msg in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        insert_into_db(id, msg, keyboard)

                    elif msg in ('отписка', 'отписаться', 'отписка от рассылки'):
                        send (event, 'Про какой уровень Q вам больше не интересно получать информацию?', keyboard_five)

                    elif msg in ('отписаться от 1', 'отписаться от 2', 'отписаться от 3', 'отписаться от 4', 'отписаться от 5', 'отписаться от 6', 'отписаться от 7', 'отписаться от 8', 'отписаться от 9', 'про 1', 'про 2', 'про 3', 'про 4', 'про 5', 'про 6', 'про про7', 'про 8', 'про 9', ):
                        delete_from_db(id, msg[-1], keyboard)

                    elif msg in ('stop', 'стоп'):
                        delete_from_db_for_id(id, keyboard)

                    elif msg == 'primary':
                        img = urllib.request.urlopen(url_picture_1, timeout = 30).read()
                        out = open("Primary.png", "wb")
                        out.write(img)
                        out.close()
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('Primary.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

                        send_attachment (event, attachment, keyboard)

                    elif msg == 'secondary (dmi)':
                        img = urllib.request.urlopen(url_picture_2, timeout = 30).read()
                        out = open("Secondary (DMI).png", "wb")
                        out.write(img)
                        out.close()
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('Secondary (DMI).png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

                        send_attachment (event, attachment, keyboard)

                    elif msg == 'k&q index':
                        img = urllib.request.urlopen(url_picture_3, timeout = 30).read()
                        out = open("K&Q index.png", "wb")
                        out.write(img)
                        out.close()
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('K&Q index.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

                        send_attachment (event, attachment, keyboard)

                    elif msg == 'all graphs':

                        img = urllib.request.urlopen(url_picture_1, timeout = 30).read()
                        out = open("Primary.png", "wb")
                        out.write(img)
                        out.close()
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('Primary.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        picture_1 = f'photo{owner_id}_{photo_id}_{access_key}'

                        img = urllib.request.urlopen(url_picture_2, timeout = 30).read()
                        out = open("Secondary (DMI).png", "wb")
                        out.write(img)
                        out.close()
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('Secondary (DMI).png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        picture_2 = f'photo{owner_id}_{photo_id}_{access_key}'

                        img = urllib.request.urlopen(url_picture_3, timeout = 30).read()
                        out = open("K&Q index.png", "wb")
                        out.write(img)
                        out.close()
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('K&Q index.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        picture_3 = f'photo{owner_id}_{photo_id}_{access_key}'

                        send_attachment (event, [picture_1, picture_2, picture_3], keyboard)

                    else:
                        if not event.from_chat:
                            send(event, 'К сожалению, я не понимаю...(', keyboard)

        except (socket.timeout, urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as err:
            print(err)
            print('Переподключение longpool')
            longpoll = VkBotLongPoll(vk_session, '202712381')


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
