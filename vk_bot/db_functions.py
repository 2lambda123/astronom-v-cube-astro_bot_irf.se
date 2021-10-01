from vk_api import VkApi
import psycopg2
from psycopg2 import Error
from config import *
from vk_api.utils import get_random_id

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
