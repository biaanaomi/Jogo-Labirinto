from os import path
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error

ROOT = path.dirname(path.relpath((__file__)))

def create_post(name, content):
    connection = mysql.connector.connect(host='localhost',
                                 database='gamedb',
                                 user='root',
                                 password='')

    sql_insert_query = ("INSERT INTO user_info(nome, tempo) VALUES (%s,%s)", (name, content))
    cursor = connection.cursor()
    result  = cursor.execute(*sql_insert_query)
    connection.commit()
    print ("Record inserted successfully into python_users table")

def get_posts():
    try:
       mySQLconnection = mysql.connector.connect(host='localhost',
                                 database='gamedb',
                                 user='root',
                                 password='')

       sql_select_Query = "SELECT * FROM user_info ORDER BY tempo ASC"
       cursor = mySQLconnection.cursor()
       cursor.execute(sql_select_Query)
       records = cursor.fetchall()

    except Error as e :
        print ("Error", e)
    finally:
        #fechando banco de dados
        if(mySQLconnection.is_connected()):
            mySQLconnection.close()
            print("conexão MySQL fechada")
    return records
