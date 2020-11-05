from flask import Flask, request
import subprocess
import time
import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
import ssl
ca_server = Flask(__name__)

@ca_server.route("/certs/serial", methods=['GET'])
def serial():
    return get_serial_number()

def get_serial_number():
    filename = "/etc/ssl/CA/serial"
    f = open(filename, "r")
    serial = f.read()
    f.close()
    return serial

@ca_server.route("/certs", methods=['POST', 'DELETE'])
def certs():
    if request.method == "POST":
        return do_new_cert(request)
    elif request.method == "DELETE":
        return revoke_certificate(request)

def do_new_cert(request):
    filename = "/tmp/"+str(time.time())
    f = open(filename, "w")
    csr = urlsafe_b64decode(request.form['csr']).decode()
    f.write(csr)
    f.close()
    subprocess.check_output("yes | openssl ca -config /etc/ssl/openssl.cnf -in "+filename+" -passin pass:ubuntu -out "+filename+".pem",stderr=subprocess.STDOUT, shell=True)
    f = open(filename+".pem","r")
    crt = f.read()
    f.close()
    os.remove(filename)
    os.remove(filename + ".pem")
    return urlsafe_b64encode(crt.encode()).decode()

def revoke_certificate(request):
    filename = "/tmp/"+str(time.time())
    f = open(filename, "w")
    csr = urlsafe_b64decode(request.form['crt']).decode()
    f.write(csr)
    f.close()
    resultRevoke = subprocess.check_output("sudo openssl ca -revoke " + filename + " -config /etc/ssl/openssl.cnf -passin pass:ubuntu", stderr=subprocess.STDOUT, shell=True)
    resultGencrl = subprocess.check_output("sudo openssl ca -gencrl -out /etc/ssl/CA/crl/crl.pem -passin pass:ubuntu", stderr=subprocess.STDOUT, shell=True)
    os.remove('/home/ubuntu/revoked.pem')
    os.remove(filename)
    resultCreate = subprocess.check_output("cat /etc/ssl/CA/cacert.pem /etc/ssl/CA/crl/crl.pem > /home/ubuntu/revoked.pem", stderr=subprocess.STDOUT, shell=True)
    return "Revocation done"
    

@ca_server.route("/certs/check", methods=["POST"])
def check_certificate():
    filename = "/tmp/"+str(time.time())
    f = open(filename, "w")
    csr = urlsafe_b64decode(request.form['crt']).decode()
    f.write(csr)
    f.close()
    try:
        result = subprocess.check_output("openssl verify -CAfile /home/ubuntu/revoked.pem -crl_check " + filename, stderr=subprocess.STDOUT, shell=True).decode()
    except subprocess.CalledProcessError as e:
        if e.returncode == 2 and ("revoked" in e.output.decode()):
            os.remove(filename)
            return "Certificate is revoked"
    os.remove(filename)
    if "OK" in result:
        return "Certificate is valid"
    else:
        return "Error"

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/ca_cert.pem', '/etc/Flask/private/ca_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/Flask/certs/cacert.pem')
    ca_server.run(debug=False, ssl_context=context, port= 443, host= '0.0.0.0')