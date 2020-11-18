import requests
import sys
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode

cafile = "/etc/Flask/certs/cacert.pem"
session = requests.Session()
session.verify = cafile
username_new_user = "Soron"


def main():
    print("---------Login---------")
    res = session.post("https://core/login", cert=('/etc/Flask/certs/core_cert.pem',
                                                   '/etc/Flask/private/core_key.pem'), data={'username': "admin", "password": "KK38O!M=HiCC20g9mS_gFgC"})
    print(res.text)
    cookie = res.cookies.get("userID")
    print(cookie)

    print("---------Admin without certificate---------")
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem',
                                                  '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem',
                                                  '/etc/Flask/private/core_key.pem'), cookies={'userID': "hello_world"})
    print(res.text)
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
    print(res.text)
    f = open("/home/ubuntu/cert.p12", "wb")
    p12 = res.text
    p12 = urlsafe_b64decode(p12.encode())
    f.write(p12)
    f.close()

    session.cookies.clear()
    print("--------------Check if it has valid cert--------------")
    res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.get("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    admin_cert = res.text
    print(admin_cert)
    session.cookies.clear()



    print("---------Login non admin---------")
    res = session.post("https://core/login", cert=('/etc/Flask/certs/core_cert.pem',
                                                   '/etc/Flask/private/core_key.pem'), data={'username': "lb", "password": "D15Licz6"})
    print(res.text)
    cookie = res.cookies.get("userID")
    print(cookie)

    print("---------Admin without certificate---------")
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem',
                                                  '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()

    print("---------Account---------")
    res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.post("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={"lastname": "Astrid", "email":"astrid@the_great.me"})
    print(res.text)
    session.cookies.clear()
    print("---------Create certificate---------")
    res = session.post("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={})
    print(res.text)
    session.cookies.clear()

    print("--------------Check if it has valid cert--------------")
    res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.get("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    non_admin_cert = res.text
    print(non_admin_cert)
    session.cookies.clear()
    print("---------Login non admin with a certificate---------")
    res = session.post("https://core/login", cert=('/etc/Flask/certs/core_cert.pem',
                                                   '/etc/Flask/private/core_key.pem'), data={'crt': non_admin_cert})
    print(res.text)
    cookie = res.cookies.get("userID")
    print(cookie)

    print("---------non_admin with certificate---------")
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem',
                                                  '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    print("--------------Revoke Cert--------------")
    res = session.delete("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    print("---------Account---------")
    res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()





    print("---------Login admin with a certificate---------")
    res = session.post("https://core/login", cert=('/etc/Flask/certs/core_cert.pem',
                                                   '/etc/Flask/private/core_key.pem'), data={'crt': admin_cert})
    print(res.text)
    cookie = res.cookies.get("userID")
    print(cookie)

    print("---------Admin with certificate---------")
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem',
                                                  '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()

    print("--------------Revoke Cert--------------")
    res = session.delete("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    print("--------------Revoke Cert--------------")
    res = session.delete("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    print("---------Account---------")
    res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()



if __name__ == "__main__":
    main()
