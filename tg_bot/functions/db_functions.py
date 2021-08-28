import psycopg2
from psycopg2 import Error
from functions.sending_functions import *
from keyboards import *
from config import *


# функция добавления пользователя в рассылку
def insert_into_db(id, q_degree):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f" INSERT INTO tg_users VALUES ({id}, {q_degree}) "
        cursor.execute(insert_query)
        connection.commit()
        send(id, 'Вы добавлены в рассылку! Теперь вы будете получать уведомления, если график достигнет или превысит значение Q, которое вы указали', standart_keyboard)
        print(f"Запись ({id}, {q_degree}) успешно вставлена")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        return send(id, 'Произошла ошибка! Вероятно, вы уже подписаны на данный уровень Q', standart_keyboard)

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
        delete_query = f" DELETE FROM tg_users WHERE id = {id} AND q_degree = {q_degree} "
        cursor.execute(delete_query)
        connection.commit()
        print("Запись успешно удалена")
        send(id, 'Вы исключены из рассылки! Больше вы не будете получать уведомления об этом уровне Q', standart_keyboard)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        send(id, 'Произошла ошибка! Вероятно, вы не подписаны на данный уровень Q', standart_keyboard)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция отключения пользователя от базы данных
def delete_from_db_for_id(id):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для удаления значения из таблицы
        delete_query = f" DELETE FROM tg_users WHERE id = {id} "
        cursor.execute(delete_query)
        connection.commit()
        print("Запись успешно удалена")
        send(id, 'Вы исключены из рассылки! Больше вы не будете получать уведомления', standart_keyboard)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        send(id, f'Произошла ошибка: {error}. Сообщите о ней в баг-репорте', standart_keyboard)


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
        insert_query = f" SELECT id FROM tg_users WHERE q_degree = {q_degree} "
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
