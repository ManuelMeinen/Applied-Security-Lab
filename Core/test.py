import requests
import sys
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode

cafile = "/etc/Flask/certs/cacert.pem"
session = requests.Session()
session.verify = cafile

def main():
    request_json = {"uid": "admin"}
    res = session.post("https://mysql/all_certs", data=json.dumps(request_json), cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    print(res.text)
if __name__ == "__main__":
    main()