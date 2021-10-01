#!/usr/bin/python
# -*- coding: utf-8 -*-
import vk_api
import time
import schedule
import logging
from threading import Thread
import urllib.request
import urllib3
import requests
import socket
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import *
from bot_vars import *
from keyboards import *
from sending_functions import *
from analise_functions import *

logging.basicConfig(filename = 'logs.log',  filemode='w', level = logging.INFO, format = ' %(asctime)s - %(levelname)s - %(message)s', encoding = "UTF-8", datefmt='%d-%b-%y %H:%M:%S')

socket.setdefaulttimeout(60)

logging.info('Лонгпулл запущен...')

vk_session = VkApi(token = main_token)
vk = vk_session.get_api()

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
