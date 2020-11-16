import requests
import sys
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode

cafile = "/etc/Flask/certs/cacert.pem"
session = requests.Session()
session.verify = cafile
username_new_user = "Soron"


def main():
    print("----------Create user admin in DB----------")
    json_add_user = '{"uid": "admin", "lastname": "Pavliv", "firstname":"Valia", "mail": "vp@imovies.ch", "pwd":"d033e22ae348aeb5660fc2140aec35850c4da997", "is_admin": true}'
    addr_add_user = 'https://mysql/add_user'
    response_add_user = session.post(addr_add_user, data=json_add_user, cert=(
        '/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    print(response_add_user.content.decode('utf-8'))

    print("---------Login---------")
    res = session.post("https://core/login", cert=('/etc/Flask/certs/core_cert.pem',
                                                   '/etc/Flask/private/core_key.pem'), data={'username': "lb", "password": "D15Licz6"})
    print(res.text)
    cookie = res.cookies.get("userID")
    print(cookie)

    print("---------Admin---------")
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem',
                                                  '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem',
                                                  '/etc/Flask/private/core_key.pem'), cookies={'userID': "hello_world"})
    print(res.text)
    session.cookies.clear()

    print("---------New User---------")
    res = session.post("https://core/admin/newuser", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={
                       "username": username_new_user, "is_admin": "false", "password": "iamTheKingOfTheWorld", "lastname": "Soron", "firstname": "TheGood", "email": "soron@dol_guldur.me"})
    print(res.text)
    session.cookies.clear()
    res = session.post("https://core/admin/newuser", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'),
                       cookies={'userID': cookie}, data={"username": username_new_user, "is_admin": "forSure", "password": "iamTheKingOfTheWorld"})
    print(res)
    session.cookies.clear()
    res = session.post("https://core/admin/newuser", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'),
                       cookies={'userID': cookie}, data={"username": username_new_user, "password": "iamTheKingOfTheWorld"})
    print(res)
    session.cookies.clear()

    print("---------Account---------")
    res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.post("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={"lastname": "Soron", "email":"my_precious@dol_guldur.me"})
    print(res.text)
    session.cookies.clear()

    print("---------Create certificate---------")
    res = session.post("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={})
    #print(res.text)
    session.cookies.clear()
    # print("--------------Check if it has valid cert--------------")
    # res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    # print(res.text)
    # session.cookies.clear()
    # res = session.get("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    # future_cert = res.text
    # print(future_cert)
    # session.cookies.clear()
    # print("--------------Revoke Cert--------------")
    # res = session.delete("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    # print(res.text)
    # session.cookies.clear()



if __name__ == "__main__":
    main()
