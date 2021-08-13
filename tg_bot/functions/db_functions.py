import psycopg2
from psycopg2 import Error
from aiogram import Bot
from secret_data import *
import asyncio

bot = Bot(token = main_token)

# функция добавления пользователя в рассылку
async def insert_into_db(id, q_degree, keyboard):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f" INSERT INTO tg_users VALUES ({id}, {q_degree}) "
        cursor.execute(insert_query)
        connection.commit()
        await bot.send_message(chat_id = id, text = 'Вы добавлены в рассылку! Теперь вы будете получать уведомления, если график достигнет или превысит значение Q, которое вы указали', reply_markup = keyboard)
        print(f"Запись ({id}, {q_degree}) успешно вставлена")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        return await bot.send_message(chat_id = id, text = 'Произошла ошибка! Вероятно, вы уже подписаны на данный уровень Q', reply_markup = keyboard)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция удаления пользователя из базы данных
async def delete_from_db(id, q_degree, keyboard):
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
        await bot.send_message(chat_id = id, text = 'Вы исключены из рассылки! Больше вы не будете получать уведомления об этом уровне Q', reply_markup = keyboard)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        await bot.send_message(chat_id = id, text = 'Произошла ошибка! Вероятно, вы не подписаны на данный уровень Q', reply_markup = keyboard)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция отключения пользователя от базы данных
async def delete_from_db_for_id(id, keyboard):
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
        await bot.send_message(chat_id = id, text = 'Вы исключены из рассылки! Больше вы не будете получать уведомления', reply_markup = keyboard)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        await bot.send_message(chat_id = id, text = 'Произошла ошибка!', reply_markup = keyboard)


    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# функция поиска пользователей по базе данных и создания списка рассылки
async def search_into_db(q_degree):
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
