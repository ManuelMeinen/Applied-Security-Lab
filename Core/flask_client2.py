import requests
import sys
from base64 import urlsafe_b64encode, urlsafe_b64decode

cafile = "/etc/Flask/certs/cacert.pem"
session = requests.Session()
session.verify = cafile

def main():
    res = session.post("https://core/login", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'username': "alex", "password": "hello"})
    print(res.text)
    cookie = res.cookies.get("userID")
    print(cookie)
    cookie_print = urlsafe_b64decode(cookie.encode()).decode()
    print(cookie_print)
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.get("https://core/admin", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': "hello_world"})
    print(res.text)
    session.cookies.clear()
    res = session.post("https://core/admin/newuser", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={"username": "Soron", "is_admin": "false", "password": "iamTheKingOfTheWorld"})
    print(res.text)
    session.cookies.clear()
    res = session.post("https://core/admin/newuser", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={"username": "Soron", "is_admin": "forSure", "password": "iamTheKingOfTheWorld"})
    print(res)
    session.cookies.clear()
    res = session.post("https://core/admin/newuser", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={"username": "Soron", "password": "iamTheKingOfTheWorld"})
    print(res)
    session.cookies.clear()
    res = session.get("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.post("https://core/account", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={"lastname": "Soron", "email":"my_precious@dol_guldur.me"})
    print(res.text)
    session.cookies.clear()
    res = session.post("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie}, data={})
    print(res.text)
    session.cookies.clear()
    res = session.get("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
    res = session.delete("https://core/account/certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), cookies={'userID': cookie})
    print(res.text)
    session.cookies.clear()
if __name__== "__main__":
    main()