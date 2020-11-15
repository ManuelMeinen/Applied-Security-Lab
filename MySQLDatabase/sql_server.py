import mysql.connector
from mysql.connector import Error



password = ''
with open('/var/www/mysql/database_password.txt', 'r') as f:
    password = f.read().rstrip('\n')
    f.close()



def get_user_info(user_id):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    
        cursor = connection.cursor()
        sql_select_query = "select lastname, firstname, email from users where users.uid = %s "
        input_data = (user_id, )
        cursor.execute(sql_select_query, input_data)
        record = cursor.fetchone()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()): 
            cursor.close()
            connection.close()
    return record

def get_admin_info(user_id):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)

        cursor = connection.cursor()
        sql_select_query = "select is_admin from admin where admin.uid = %s "
        input_data = (user_id, )
        cursor.execute(sql_select_query, input_data)
        record = cursor.fetchone()
    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()): 
            cursor.close()
            connection.close()
    return record


def get_password(user_id):
    record =None

    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_select_query = "select pwd from users where uid = %s "
        input_data = (user_id, )
        cursor.execute(sql_select_query, input_data)
        record = cursor.fetchone()

        print(record)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record

def update_user_data(user_id, lastname, firstname, mail, pwd, is_admin):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_update_query = "update users set lastname= %s , firstname= %s , email= %s , pwd= %s where uid= %s "
        input_data = (lastname, firstname, mail, pwd, user_id)
        cursor.execute(sql_update_query, input_data)
        connection.commit()

        sql_update_is_admin = "update admin set is_admin= %s where uid= %s "
        input_data = (is_admin, user_id)
        cursor.execute(sql_update_query, input_data)
        connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    
    return record


def add_user(user_id, lastname, firstname, mail, pwd, is_admin):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_add_user_query = "insert into users values (%s, %s, %s, %s, %s)"
        input_data = (user_id, lastname, firstname, mail, pwd)
        cursor.execute(sql_add_user_query, input_data)
        connection.commit()

        sql_add_user_query = "insert into admin values (%s, %s)"
        input_data = (user_id, is_admin)
        cursor.execute(sql_add_user_query, input_data)
        connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
        print(str(e))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

    return 0


def add_certificate(user_id, certificate):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_add_user_query = "insert into certificates values (%s, %s, 0)"
        input_data = (user_id, certificate)
        cursor.execute(sql_add_user_query, input_data)
        connection.commit()

        sql_select_query = "select * from certificates where certificates.certificate = %s "
        input_data=(certificate, )
        cursor.execute(sql_select_query, input_data)
        record = cursor.fetchone()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record


def delete_certificate(certificate):
    deleted = False
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_delete_user_query = "Update certificates set revoked=1 where certificate = %s "
        input_data = (certificate, )
        cursor.execute(sql_delete_user_query, input_data)
        connection.commit()

        sql_select_query = "select * from certificates where certificate = %s "
        input_data = (certificate, )
        cursor.execute(sql_select_query, input_data)
        records = cursor.fetchall()
        if len(records) == 0:
            deleted=True


    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

    
    return deleted

def get_uid_from_cert(certificate):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_select_query = "select uid from certificates where certificate = %s "
        input_data = (certificate, )
        cursor.execute(sql_select_query, input_data)
        record = cursor.fetchone()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record


def get_certs(uid):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_select_query = "select certificate from certificates where uid = %s"
        input_data = (uid, )
        cursor.execute(sql_select_query, input_data)
        record = cursor.fetchall()

        print(record, type(record))

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record


def get_stats():
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password=password)
    

        cursor = connection.cursor()
        sql_select_query = "select count(*), sum(revoked = 1) from certificates"

        cursor.execute(sql_select_query)
        record = cursor.fetchall()


    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record

