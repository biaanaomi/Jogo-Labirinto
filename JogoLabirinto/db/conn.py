import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error

def disp():
    try:
       mySQLconnection = mysql.connector.connect(host='localhost',
                                 database='gamedb',
                                 user='root',
                                 password='')

       sql_select_Query = "SELECT * FROM user_info ORDER BY tempo ASC"
       cursor = mySQLconnection.cursor()
       cursor.execute(sql_select_Query)
       records = cursor.fetchall()

       print("Total num de linhas: - ", cursor.rowcount)
     
       #for row in records:
       #    print(row[0],"\t",row[1],"\t""\n")

       cursor.close()
       
    except Error as e :
        print ("Error", e)
    finally:
        #fechando banco de dados
        if(mySQLconnection.is_connected()):
            mySQLconnection.close()
            print("conexão MySQL fechada")

def insert(nome,tempo):
    try:
       connection = mysql.connector.connect(host='localhost',
                                 database='gamedb',
                                 user='root',
                                 password='')

       sql_insert_query = ("INSERT INTO user_info(nome, tempo) VALUES (%s,%s)", (nome, tempo))

       cursor = connection.cursor()
       result  = cursor.execute(*sql_insert_query)
       connection.commit()
       print ("Record inserido com sucesso")

    except mysql.connector.Error as error :
        connection.rollback() #rollback para exceção
        print("Falhou {}".format(error))

    finally:
        #fechando conexão com db
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")            


disp()