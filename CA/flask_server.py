from flask import Flask, request
import time
import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
import ssl
ca_server = Flask(__name__)

@ca_server.route("/certs", methods=['GET','POST'])
def certs():
    if request.method == "POST":
        return do_new_cert(request)
    elif request.method == "GET":
        return get_serial_number()

def do_new_cert(request):
    filename = "/tmp/"+str(time.time())
    f = open(filename, "w")
    csr = urlsafe_b64decode(request.form['csr']).decode()
    f.write(csr)
    f.close()
    os.system("yes | openssl ca -config /etc/ssl/openssl.cnf -in "+filename+" -passin pass:ubuntu -out "+filename+".pem")
    f = open(filename+".pem","r")
    crt = f.read()
    f.close()
    os.system("rm " + filename)
    os.system("rm " + filename + ".pem")
    return crt

def get_serial_number():
    filename = "/etc/ssl/CA/serial"
    f = open(filename, "r")
    serial = f.read()
    f.close()
    return serial

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/ca_cert.pem', '/etc/Flask/private/ca_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/ssl/CA/cacert.pem')
    ca_server.run(debug=False, ssl_context=context, port= 443, host= '0.0.0.0')