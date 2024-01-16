import psycopg2
""" connection = psycopg2.connect(user = user, password = password, host = host, port = port, database = database) """

connection = psycopg2.connect(user = 'postgres', password = 'postgres', host = 'localhost', port = '5432', database = 'astro_bot_irf.se')


""" # Курсор для выполнения операций с базой данных
cursor = connection.cursor()
insert_query = f"INSERT INTO tg_users VALUES ({55555555}, {1})"
cursor.execute(insert_query)
connection.commit() """