import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = (BASE_DIR + '\\management.db')


def get_amount(id):
    connection = sqlite3.connect(db_dir)
    cursor = connection.cursor()
    sql_query = "select amount from amounts where person_id =  " + str(id)
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    returned_amount = 0
    for registro in result:
        returned_amount = registro
    return returned_amount[0]


def send_to_failure(step, origin, destination, amount):
    connection = sqlite3.connect(db_dir)
    cursor = connection.cursor()
    sql_query = "insert into failure(step_id, origin, destination, amount) "
    sql_query += "values(" + str(step) + "," + str(origin) + "," + str(destination) + "," + str(amount) + ")"
    cursor.execute(sql_query)
    connection.commit()
    connection.close()


def update_amount(id, amount):
    connection = sqlite3.connect(db_dir)
    cursor = connection.cursor()
    sql_query = "update amounts set amount = " + str(amount) + " where person_id = " + str(id)
    cursor.execute(sql_query)
    connection.commit()
    connection.close()
