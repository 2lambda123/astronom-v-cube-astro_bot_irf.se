#!/usr/bin/python
# -*- coding: utf-8 -*-
import vk_api
import urllib.request
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from astro_bot_vars import *

print ('Бот запущен...')

keyboard = VkKeyboard(one_time=True)

keyboard.add_button('Primary', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Secondary (DMI)', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()  # Переход на вторую строку
keyboard.add_button('K&Q index', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('All', color=VkKeyboardColor.PRIMARY)

vk_session = VkApi(token = main_token)
longpoll = VkBotLongPoll(vk_session, '202712381')
vk = vk_session.get_api()

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


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        print('-' * 30)
        print(f'Сообщение получено от id: ' + str({event.obj["peer_id"]}) )
        print('Текст сообщения: ' + str(event.object['text']))
        print('-' * 30)

        msg = event.object['text'].lower()

        if msg in ('команды', 'начать'):
            send (event, commands)

        elif msg in ('test', 'тест'):
            send (event, 'Бот работает успешно!')

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
