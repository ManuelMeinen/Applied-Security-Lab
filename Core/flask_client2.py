import requests
import sys
from base64 import urlsafe_b64encode, urlsafe_b64decode

cafile = "/home/ubuntu/cacert.pem"
session = requests.Session()
session.verify = cafile

def main():
    res = session.post("https://core/login", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'username': "alex", "password": "hello"})
    print(res.text)
    cookie = res.cookies.get("userID")
    print(cookie)
    cookie = urlsafe_b64decode(cookie.encode()).decode()
    print(cookie)
if __name__== "__main__":
    main()