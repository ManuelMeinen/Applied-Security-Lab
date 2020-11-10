import requests
import time
import json

from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to MySQL server!'
    


if __name__ == '__main__':
    time.sleep(3)
    json_id = '{"uid": "ms"}'

    # GET PASSWORD GIVEN UID
    addr_password = 'http://127.0.0.1:5000/password'
    response_pwd = requests.post(addr_password, json_id)
    print(json.loads(response_pwd.content.decode('utf-8'))['pwd'])

    print("--------------------------------------")

    # GET ALL INFO GIVEN UID
    addr_get_info = 'http://127.0.0.1:5000/get_info'
    response_infos = requests.post(addr_get_info, json_id)
    print(json.loads(response_infos.content.decode('utf-8')))

    print("--------------------------------------")

    # UPDATE USER INFO GIVEN UID AND FIELDS TO UPDATE
    json_update = '{"uid": "ms", "mail": "ms@imovies.ch", "is_admin": false}'
    addr_update = 'http://127.0.0.1:5000/update'
    response_update = requests.post(addr_update, json_update)
    print(json.loads(response_update.content.decode('utf-8')))

    print("--------------------------------------")

    # ADD USER TO USERS DATABASE
    #si pas de uid ou de pwd, le user sera pas ajouté
    json_add_user = '{"uid": "vp", "lastname": "Pavliv", "firstname":"Valia", "mail": "vp@imovies.ch", "pwd":"2j3h5k23bk5rb2k3", "is_admin": true}'
    addr_add_user = 'http://127.0.0.1:5000/add_user'
    response_add_user = requests.post(addr_add_user, json_add_user)
    print(json.loads(response_add_user.content.decode('utf-8')))

    print("--------------------------------------")

    #DELETE USER FROM USER AND CERTIFICATE DATABASE GIVEN UID
    #si deleted return 0, si problème return 1
    addr_delete_user = 'http://127.0.0.1:5000/delete_user'
    json_id = '{"uid": "vp"}'
    response_delete_user = requests.post(addr_delete_user, json_id)
    print(json.loads(response_delete_user.content.decode('utf-8')))

    print("--------------------------------------")

    # ADD USER CERTIFICATE
    json_add_user = '{"uid": "ms", "certificate": "ugiwdfxiuiwgcdzu"}'
    addr_add_user = 'http://127.0.0.1:5000/add_user_certificate'
    response_add_user = requests.post(addr_add_user, json_add_user)
    print(json.loads(response_add_user.content.decode('utf-8')))

    print("--------------------------------------")

    # DELETE USER CERTIFICATE
    json_delete_cert = '{"certificate": "ugiwdfxiuiwgcdzu"}'
    addr_delete_cert = 'http://127.0.0.1:5000/delete_user_certificate'
    response_delete_certificate = requests.post(addr_delete_cert, json_delete_cert)
    print(json.loads(response_delete_user.content.decode('utf-8')))

    print("--------------------------------------")

    
    #ADD ANOTHER ROW TO CERTIFICATE TABLE
    json_add_user = '{"uid": "lb", "certificate": "ajsdcnifasuev"}'
    addr_add_user = 'http://127.0.0.1:5000/add_user_certificate'
    response_add_user = requests.post(addr_add_user, json_add_user)
    print(json.loads(response_add_user.content.decode('utf-8')))
    
    
    #GET UID OF THIS CERTIFICATE
    json_cert = '{"certificate": "ajsdcnifasuev"}'
    addr_get_uid = 'http://127.0.0.1:5000/who_has_this_cert'
    response_uid = requests.post(addr_get_uid, json_add_user)
    print(json.loads(response_uid.content.decode('utf-8')))

    
    print("--------------------------------------")

    
    #ADD ANOTHER ROW TO CERTIFICATE TABLE
    json_add_user = '{"uid": "lb", "certificate": "ymnfkjewioqojs"}'
    addr_add_user = 'http://127.0.0.1:5000/add_user_certificate'
    response_add_user = requests.post(addr_add_user, json_add_user)
    print(json.loads(response_add_user.content.decode('utf-8')))
    


    #GET ALL CERTIFICATES OF A USER
    json_uid = '{"uid": "lb"}'
    addr_all_certs = 'http://127.0.0.1:5000/all_certs'
    response_all_certs = requests.post(addr_all_certs, json_uid)
    print(json.loads(response_all_certs.content.decode('utf-8')))





    
    print("--------------------------------------")
    print("--------------------------------------")
    print("--------------------------------------")
    print("DELETE ALL ADDED STUFF")
    json_delete_cert = '{"certificate": "ajsdcnifasuev"}'
    addr_delete_cert = 'http://127.0.0.1:5000/delete_user_certificate'
    response_delete_certificate = requests.post(addr_delete_cert, json_delete_cert)
    print(json.loads(response_delete_user.content.decode('utf-8')))

    json_delete_cert = '{"certificate": "ymnfkjewioqojs"}'
    addr_delete_cert = 'http://127.0.0.1:5000/delete_user_certificate'
    response_delete_certificate = requests.post(addr_delete_cert, json_delete_cert)
    print(json.loads(response_delete_user.content.decode('utf-8')))
    














    


    #app.run(host='10.0.20.30', port=5001)