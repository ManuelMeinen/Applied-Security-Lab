import requests
import time
import json

from flask import Flask, request


app = Flask(__name__)
cafile = "/etc/Flask/certs/cacert.pem"
session = requests.Session()
session.verify = cafile


@app.route('/')
def hello():
    return 'Welcome to MySQL server!'
    


if __name__ == '__main__':
    time.sleep(3)
    json_id = '{"uid": "ms"}'

    
    # GET PASSWORD GIVEN UID

    
    print('\x1b[6;30;42m' + 'GETTING PASSWORD' + '\x1b[0m')
    addr_password = 'https://mysql/password'
    response_pwd = session.post(addr_password, data=json_id, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(response_pwd.content.decode('utf-8'))

    print("--------------------------------------")
    

    # GET ALL INFO GIVEN UID
    print('\x1b[6;30;42m' + 'GETTING USERS INFOS' + '\x1b[0m')
    addr_get_info = 'https://mysql/get_info'
    response_infos = session.post(addr_get_info, data=json_id, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(json.loads(response_infos.content.decode('utf-8')))

    print("--------------------------------------")

    # UPDATE USER INFO GIVEN UID AND FIELDS TO UPDATE
    print('\x1b[6;30;42m' + 'UPDATE USERS INFOS' + '\x1b[0m')
    json_update = '{"uid": "ms", "mail": "ms@imovies.ch", "is_admin": false, "pwd": "newpassword"}'
    addr_update = 'https://mysql/update'
    response_update = session.post(addr_update, data=json_update, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(response_update.content.decode('utf-8'))

    print("--------------------------------------")

    # ADD USER TO USERS DATABASE
    print('\x1b[6;30;42m' + 'ADD A USER' + '\x1b[0m')
    #si pas de uid ou de pwd, le user sera pas ajouté
    json_add_user = '{"uid": "vp", "lastname": "Pavliv", "firstname":"Valia", "mail": "vp@imovies.ch", "pwd":"2j3h5k23bk5rb2k3", "is_admin": true}'
    addr_add_user = 'https://mysql/add_user'
    response_add_user = session.post(addr_add_user, data=json_add_user, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    is_user_added = session.post(addr_get_info, data='{"uid": "vp"}', cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(response_add_user.content.decode('utf-8'))
    print(json.loads(is_user_added.content.decode('utf-8')))


    print("--------------------------------------")


    # ADD USER CERTIFICATE
    print('\x1b[6;30;42m' + 'ADD USER CERTIFICATE' + '\x1b[0m')
    json_add_user = '{"uid": "vp"}'
    addr_add_user = 'https://mysql/add_user_certificate'
    response_add_user = session.post(addr_add_user, data=json_add_user, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(response_add_user.content.decode('utf-8'))

    json_add_user = '{"uid": "vp", "certificate": "1234aouhfdu"}'
    addr_add_user = 'https://mysql/add_user_certificate'
    response_add_user = session.post(addr_add_user, data=json_add_user, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    

    print("--------------------------------------")

    # REVOKE USER CERTIFICATE
    print('\x1b[6;30;42m' + 'REVOKE USER CERTIFICATE' + '\x1b[0m')
    json_delete_cert = '{"certificate": "1234aouhfdu"}'
    addr_delete_cert = 'https://mysql/revoke_user_certificate'
    response_delete_certificate = session.post(addr_delete_cert, data=json_delete_cert, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(response_delete_certificate.content.decode('utf-8'))

    print("--------------------------------------")

    
    #GET UID OF THIS CERTIFICATE
    print('\x1b[6;30;42m' + 'GETTING UID FROM CERTIFICATE' + '\x1b[0m')
    json_cert = '{"certificate": "1234aouhfdu"}'
    addr_get_uid = 'https://mysql/who_has_this_cert'
    response_uid = session.post(addr_get_uid, data=json_add_user, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(json.loads(response_uid.content.decode('utf-8')))

    
    print("--------------------------------------")


    #GET ALL CERTIFICATES OF A USER
    print('\x1b[6;30;42m' + 'GETTING ALL CERTIFIACTES OF A USER' + '\x1b[0m')
    json_uid = '{"uid": "a3"}'
    addr_all_certs = 'https://mysql/all_certs'
    response_all_certs = session.post(addr_all_certs, data=json_uid, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(response_all_certs.content.decode('utf-8'))


    print("--------------------------------------")

    

    #GET STATS
    print('\x1b[6;30;42m' + 'GETTING ALL STATS ABOUT CERTIFICATES' + '\x1b[0m')
    addr_stats = 'https://mysql/certs_stats'
    response_stats = session.post(addr_stats, cert=('/etc/Flask/certs/mysql_cert.pem', '/etc/Flask/private/mysql_key.pem'))
    print(json.loads(response_stats.content.decode('utf-8')))