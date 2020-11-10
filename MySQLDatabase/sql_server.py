import mysql.connector

from mysql.connector import Error


def get_user_info(user_id):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_select_query = "select lastname, firstname, email, is_admin from users where users.uid = '"+user_id+"'"

        cursor.execute(sql_select_query)
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
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_select_query = "select pwd from users where users.uid = '"+user_id+"'"

        cursor.execute(sql_select_query)
        record = cursor.fetchone()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record

def update_user_data(user_id, lastname, firstname, mail, is_admin):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_update_query = "update users set lastname= %s , firstname= %s , email= %s , is_admin= %s where uid= %s "
        input_data = (lastname, firstname, mail, is_admin, user_id)
        cursor.execute(sql_update_query, input_data)
        connection.commit()

        sql_select_query = "select lastname, firstname, email, is_admin from users where users.uid = '"+user_id+"'"

        cursor.execute(sql_select_query)
        record = cursor.fetchone()

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
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_add_user_query = "insert into users values (%s, %s, %s, %s, %s, %s)"
        input_data = (user_id, lastname, firstname, mail, pwd, is_admin)
        cursor.execute(sql_add_user_query, input_data)
        connection.commit()



        sql_select_query = "select lastname, firstname, email, is_admin from users where users.uid = '"+user_id+"'"

        cursor.execute(sql_select_query)
        record = cursor.fetchone()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record

def delete_user(user_id):

    deleted_from_users = False
    deleted_from_certificates = False
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    


        cursor = connection.cursor()
        sql_delete_user_query = "delete from users where uid = '"+user_id+"' "
        cursor.execute(sql_delete_user_query)
        connection.commit()

        sql_select_query = "select * from users where uid = '"+user_id+"' "
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        if len(records) == 0:
            deleted_from_users=True

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_delete_user_query = "Delete from certificates where uid = '"+user_id+"' "
        cursor.execute(sql_delete_user_query)
        connection.commit()

        sql_select_query = "select * from certificates where uid = '"+user_id+"' "
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        if len(records) == 0:
            deleted_from_certificates=True


    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

    
    return (deleted_from_certificates and deleted_from_users)

def add_certificate(user_id, certificate):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_add_user_query = "insert into certificates values (%s, %s)"
        input_data = (user_id, certificate)
        cursor.execute(sql_add_user_query, input_data)
        connection.commit()

        sql_select_query = "select * from certificates where certificates.certificate = '"+certificate+"'"
        cursor.execute(sql_select_query)
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
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_delete_user_query = "Delete from certificates where certificate = '"+certificate+"' "
        cursor.execute(sql_delete_user_query)
        connection.commit()

        sql_select_query = "select * from certificates where certificate = '"+certificate+"' "
        cursor.execute(sql_select_query)
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
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_select_query = "select uid from certificates where certificate = '"+certificate+"'"

        cursor.execute(sql_select_query)
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
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_select_query = "select certificate from certificates where uid = '"+uid+"'"

        cursor.execute(sql_select_query)
        record = cursor.fetchall()

        print(record, type(record))

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record



