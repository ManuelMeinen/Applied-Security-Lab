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
        sql_select_query = """select lastname, firstname, email from users where users.uid = %s"""
        cursor.execute(sql_select_query,(user_id,))
        record = cursor.fetchone()

        # cursor = connection.cursor()
        # sql_select_query = "select lastname, firstname, email, is_admin from users where users.uid = '"+user_id+"'"

        # cursor.execute(sql_select_query)
        # record = cursor.fetchone()

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
                                            password='JT:*g,m,p8{-"95')

        cursor = connection.cursor()
        sql_select_query = "select is_admin from admin where admin.uid = '"+user_id+"'"

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

        print(record)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return record

def update_user_data(user_id, lastname, firstname, mail, password, is_admin):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_update_query = "update users set lastname= %s , firstname= %s , email= %s , pwd= %s where uid= %s "
        input_data = (lastname, firstname, mail, password, user_id)
        cursor.execute(sql_update_query, input_data)
        connection.commit()

        sql_update_is_admin = "update admin set is_admin= %s where uid= %s "
        input_data = (is_admin, user_id)
        cursor.execute(sql_update_query, input_data)
        connection.commit()

        sql_select_query = "select lastname, firstname, email from users where users.uid = %s"
        input_data = (user_id,)
        cursor.execute(sql_select_query, input_data)
        record1 = cursor.fetchone()

        sql_select_query = "select is_admin from admin where admin.uid = %s"
        input_data = (user_id,)
        cursor.execute(sql_select_query, input_data)
        record2 = cursor.fetchone()

        record = (record1[0], record1[1], record1[2], record2[0])

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

    #TODO return ok
    return 0


def add_certificate(user_id, certificate):
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    

        cursor = connection.cursor()
        sql_add_user_query = "insert into certificates values (%s, %s, 0)"
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
        sql_delete_user_query = "Update certificates set revoked=1 where certificate = '"+certificate+"' "
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


def get_stats():
    record =None
    try:
        connection = mysql.connector.connect(host='localhost', 
                                            database='imovies',
                                            user='ubuntu', 
                                            password='JT:*g,m,p8{-"95')
    

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





