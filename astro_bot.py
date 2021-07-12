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
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from secret_data import *
from astro_bot_vars import *

print ('Бот запущен...')

keyboard = VkKeyboard(one_time = True)

keyboard.add_button('Primary', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Secondary (DMI)', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()  # Переход на вторую строку
keyboard.add_button('K&Q index', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('All', color=VkKeyboardColor.PRIMARY)

vk_session = VkApi(token = main_token)
longpoll = VkBotLongPoll(vk_session, '202712381')
vk = vk_session.get_api()


# функция добавления пользователя в рассылку
def insert_into_db(id, q_degree):
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
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы добавлены в рассылку! Теперь вы будете получать уведомления, если график достигнет значения Q, которое вы указали')

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка! Вероятно, вы уже подписаны на данный уровень Q')

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция удаления пользователя из базы данных
def delete_from_db(id, q_degree):
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
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Вы исключены из рассылки! Больше вы не будете получать уведомления')

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        vk.messages.send(random_id = get_random_id(), peer_id = id, keyboard = keyboard.get_keyboard(), message = 'Произошла ошибка! Вероятно, вы не подписаны на данный уровень Q')

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
def send(event, msg):

    if event.obj['peer_id'] > 2e9:       #если чат
        print(f'Ответил: "{msg}" для беседы с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], message = msg)
    else:
        print(f'Ответил: "{msg}" для пользователя с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], keyboard = keyboard.get_keyboard(), message = msg)


# функция отправки сообщения с фото
def send_attachment(event, image):

    if event.obj['peer_id'] > 2e9:       #если чат
        print(f'Отправил фото для беседы с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], attachment = image)
    else:
        print(f'Отправил фото для пользователя с id: {event.obj["peer_id"]}')
        return vk.messages.send(random_id = get_random_id(), peer_id = event.obj['peer_id'], keyboard = keyboard.get_keyboard(), attachment = image)


# функция рассылки оповещения
def sending(degree):

    list_id = search_into_db(degree)

    for id_one in list_id:
        vk.messages.send(random_id = get_random_id(), peer_id = id_one, keyboard = keyboard.get_keyboard(), message = f'&#10071;Внимание! График достиг уровня {degree}&#10071;')

    print(f'Ответил: "График достиг уровня {degree}"')

# функция проверки графика и высылания ответа с анализом
def graphs_analise(degree):

    img = urllib.request.urlopen(url_picture_3).read()
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
        print('Вижу не белый')
        sending(degree)

    else:
        print('Белый вижу')


# функция отправки результата анализа по базам данных
def analise_sender():
    while True:
        print('Функция анализа работает нормально')
        graphs_analise(1)
        graphs_analise(2)
        graphs_analise(3)
        graphs_analise(4)
        graphs_analise(5)
        time.sleep(900)


# функция прослушивания longpoll и ответа на ключевые слова
def job_longpool():
    print('Функция прослушивания longpool запущена')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('-' * 30)
            print(f'Сообщение получено от id: ' + str({event.obj["peer_id"]}) )
            print('-' * 30)
            print('Текст сообщения: ' + str(event.object['text']))
            print('-' * 30)

            msg = event.object['text'].lower()
            id = event.obj["peer_id"]

            if msg in ('команды', 'начать', 'привет', 'старт'):
                send (event, commands)

            elif msg in ('test', 'тест'):
                send (event, 'Бот работает успешно!')

            elif 'помощь' in msg or 'help' in msg:
                vk.messages.send(random_id = get_random_id(), peer_id = 557660245, message = (f'&#10071;БАГ-РЕПОРТ&#10071; {event}'))
                send (event, 'Ваш баг-репорт отправлен разработчику бота, в ближайшее время он займется исправлением неисправности. Спасибо :)')

            elif msg in ('уровни', 'уровни q', 'уровень', 'уровень q', 'q'):
                send (event, degree_Q)

            elif msg in ('рассылка', 'подписка', 'подписка на рассылку', 'подписаться'):
                send (event, 'Какой уровень Q вас интересует? (Узнать уровень Q для вашей широты можно, написав мне слово "Уровни")')

            elif msg in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                insert_into_db(id, msg)

            elif msg in ('отписка', 'отписаться', 'отписка от рассылки'):
                send (event, 'Про какой уровень Q вам больше не интересно получать информацию? (напишите "отписаться от {цифра}")')

            elif msg in ('отписаться от 1', 'отписаться от 2', 'отписаться от 3', 'отписаться от 4', 'отписаться от 5', 'отписаться от 6', 'отписаться от 7', 'отписаться от 8', 'отписаться от 9'):
                delete_from_db(id, msg[-1])

            elif msg == 'primary':
                img = urllib.request.urlopen(url_picture_1).read()
                out = open("Primary.png", "wb")
                out.write(img)
                out.close()
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('Primary.png')
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'

                send_attachment (event, attachment)

            elif msg == 'secondary (dmi)':
                img = urllib.request.urlopen(url_picture_2).read()
                out = open("Secondary (DMI).png", "wb")
                out.write(img)
                out.close()
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('Secondary (DMI).png')
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'

                send_attachment (event, attachment)

            elif msg == 'k&q index':
                img = urllib.request.urlopen(url_picture_3).read()
                out = open("K&Q index.png", "wb")
                out.write(img)
                out.close()
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('K&Q index.png')
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'

                send_attachment (event, attachment)

            elif msg == 'all':

                img = urllib.request.urlopen(url_picture_1).read()
                out = open("Primary.png", "wb")
                out.write(img)
                out.close()
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('Primary.png')
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                picture_1 = f'photo{owner_id}_{photo_id}_{access_key}'

                img = urllib.request.urlopen(url_picture_2).read()
                out = open("Secondary (DMI).png", "wb")
                out.write(img)
                out.close()
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('Secondary (DMI).png')
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                picture_2 = f'photo{owner_id}_{photo_id}_{access_key}'

                img = urllib.request.urlopen(url_picture_3).read()
                out = open("K&Q index.png", "wb")
                out.write(img)
                out.close()
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('K&Q index.png')
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                picture_3 = f'photo{owner_id}_{photo_id}_{access_key}'

                send_attachment (event, [picture_1, picture_2, picture_3])

            else:
                if not event.from_chat:
                    send(event, 'К сожалению, я не понимаю...(')

th_1 = Thread(target = analise_sender)
th_2 = Thread(target = job_longpool)

# функция запуска многопоточной работы бота
if __name__ == '__main__':
    th_1.start()
    th_2.start()
# schedule.every().minute.at(":17").do(job)
