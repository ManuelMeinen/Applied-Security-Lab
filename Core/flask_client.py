import requests
cafile = "/home/ubuntu/cacert.pem"
session = requests.Session()
session.verify = cafile
res = session.get("https://ca_server/", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
print(res.text)