import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = (BASE_DIR + '\\taker.db')

def get_amount(id): 
    connection = sqlite3.connect(db_dir)
    cursor = connection.cursor()
    sql_query = "select a.amount from amounts a, people p where a.person_id = p.id and p.id = " + str(id)
    cursor.execute(sql_query)
    results = cursor.fetchall()
    connection.close()
    return results

def take(id, amount_to_take):    
    connection = sqlite3.connect(db_dir)
    cursor = connection.cursor()
    sql_query = "update amounts set amount = amount - " + str(amount_to_take) + " where person_id = " + str(id)
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
