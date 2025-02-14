from flask import Flask, request, make_response
import requests
from base64 import urlsafe_b64encode, urlsafe_b64decode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates, load_key_and_certificates
from cryptography import x509
from cryptography.x509.oid import NameOID

from hashlib import sha1
import uuid
import json
import time
import os
import ssl
core_server = Flask(__name__)
private_key = None
public_key = None
cafile = "/etc/Flask/certs/cacert.pem"
session = requests.Session()
session.verify = cafile
MAX_AGE = 60*10
pkcs_12_password = "asl"

@core_server.route("/login", methods=["POST"])
def login():
    # Cookie is JSON with username, timestamp, nonce, signed hash of the three information => base64
    username = request.form.get("username")
    password = request.form.get("password")
    certificate = request.form.get("crt")
    username = check_user_credential(username, password, certificate)
    if(not username):
        return "Authentication failed", 403
    timestamp = str(time.time())
    nonce = str(uuid.uuid4().hex)
    withCert = "true" if certificate!=None else "false"
    message = username + timestamp + nonce + withCert
    message = message.encode()
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    cookie = {
        "username": username,
        "timestamp": timestamp,
        "nonce": nonce,
        "withCert": withCert,
        "signature": urlsafe_b64encode(signature).decode()
    }
    cookie = urlsafe_b64encode(json.dumps(cookie).encode()).decode()
    res = make_response("Hello " + username)
    res.set_cookie("userID", cookie, max_age=MAX_AGE)
    return res

@core_server.route("/admin", methods=["GET"])
def admin():
    check, username = check_cookie(request)
    
    if check and check_is_admin(username) and check_connected_with_cert(request):
        res = session.get("https://ca_server:10443/certs/serial", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
        serial = res.text.replace("\n","")
        issuedCert, revokedCert = statistics_certificates()
        stat = {
            "serial":  serial,
            "nbreissued": issuedCert,
            "nbrerevoked": revokedCert
        }
        return json.dumps(stat)
    else:
        return "Authentication Failed", 403

@core_server.route("/account", methods=["GET", "POST"])
def get_account_info():
    # global users
    check, username = check_cookie(request)
    if check: 
        username_json = {"uid": username}
        res = session.post("https://mysql:10443/get_info", data=json.dumps(username_json), cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
        if res.status_code == 404 or res.status_code == 400:
            return "User not known", 404
        res = json.loads(res.content)
        if request.method == "POST":
            user = {}
            user["uid"] = username
            user["lastname"] = request.form.get("lastname") if request.form.get("lastname") != None else res["lastname"]
            user["firstname"] = request.form.get("firstname") if request.form.get("firstname") != None else res["firstname"]
            user["mail"] = request.form.get("email") if request.form.get("email") != None else res["mail"]
            # Add possibility to modify password
            if request.form.get("password"):
                user["pwd"] = hash_password(request.form.get("password"))
            res = session.post("https://mysql:10443/update", data=json.dumps(user), cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
            if res.status_code == 404 or res.status_code == 400:
                return "User not known", 404
            if res.status_code == 520:
                return "Internal Error: User not updated", 500
            res = json.loads(res.content)
        response = {
            "username": username,
            "lastname": res["lastname"],
            "firstname": res["firstname"],
            "email": res["mail"],
            "has_certificate_available": has_valid_certificate(username) != None
            }
        return json.dumps(response)
    return "Authentication Failed", 403


@core_server.route("/account/certificate", methods=["GET", "POST", "DELETE"])
def manage_certificate():
    check, username = check_cookie(request)
    if check:
        if request.method == "GET":
            cert = has_valid_certificate(username)
            if cert== None:
                return "No valid certificate", 404
            return refactor_certificate(cert)
        
        elif request.method == "POST":
            if has_valid_certificate(username) != None:
                return "A valid cert already exists", 400
            [private_key, csr] = create_CSR(username)
            res = session.post("https://ca_server:10443/certs", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'csr': csr})
            if(res.status_code != 200):
                return "Error was not added", 500
            crt = "-----BEGIN CERTIFICATE-----" + res.text.split("-----BEGIN CERTIFICATE-----")[1]
            crt_db = crt.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").strip().replace("\n","")
            if add_certificate(username, crt_db) != 200:
                res = session.delete("https://ca_server:10443/certs", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'crt': res.text})
                return "Error was not added", 500
            pkcs12 = create_pkcs12(username, private_key, crt)
            save_private_key(username, private_key)
            return pkcs12
        elif request.method == "DELETE":
            cert = has_valid_certificate(username)
            if cert != 0:
                res1 = session.delete("https://ca_server:10443/certs", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'crt': refactor_certificate(cert)})
                if res1.status_code != 200:
                    return "Certificate not revoked", 500
                payload_cert = {'certificate': cert}
                res2 = session.post("https://mysql:10443/revoke_user_certificate", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data=json.dumps(payload_cert))
                if res2.status_code != 200:
                    return "Certificate not revoked", 500
                return "Success"
            else:
                return "No valid certificate to revoke", 400
    return "Authentication Failed", 403

def refactor_certificate(cert):
    return "-----BEGIN CERTIFICATE-----\n" + cert + "\n-----END CERTIFICATE-----"

@core_server.route("/revocation_list", methods=["GET"])
def revocations_list():
    revoked = session.get("https://ca_server:10443/revocation_list", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    return revoked.content

def check_cookie(request):
    try: 
        cookie = request.cookies.get("userID")
        cookie = json.loads(urlsafe_b64decode(cookie.encode()).decode())
        username = cookie["username"]
        timestamp = cookie["timestamp"]
        nonce = cookie["nonce"]
        withCert = cookie["withCert"]
        signature = urlsafe_b64decode(cookie["signature"].encode())
        message = username + timestamp + nonce + withCert
        message = message.encode()
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # Cookie not valid after MAX_AGE seconds
        if(time.time() - float(timestamp) > MAX_AGE):
            return False, None
    except:
        return False, None

    return True, username

def check_is_admin(username):
    username_json = {"uid": username}
    res = session.post("https://mysql:10443/get_info", data=json.dumps(username_json), cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    if res.status_code == 404 or res.status_code == 400:
        return False
    is_admin = json.loads(res.content)["is_admin"]
    return is_admin == 'true'

def check_connected_with_cert(request):
    cookie = request.cookies.get("userID")
    cookie = json.loads(urlsafe_b64decode(cookie.encode()).decode())
    return cookie["withCert"] == "true"

def check_user_credential(username, password, certificate):
        if certificate:
            return find_username_by_cert(certificate)
        if password:
            password = hash_password(password)
            json_id = '{"uid": "'+ username +'"}'
            res = session.post("https://mysql:10443/password", data=json_id, cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
            if res.status_code == 404 or res.status_code == 400:
                return None
            storedPwd = json.loads(res.content)['pwd']
            if password == storedPwd:
                return username
        return None

def find_username_by_cert(cert):
    cert = cert.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n","").replace("\t","").strip()
    request_json = {"uid": "admin"}
    json_id = '{"certificate": "'+ cert +'"}'
    res = session.post("https://mysql:10443/who_has_this_cert", data=json_id, cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    if res.status_code == 404 or res.status_code == 400:
        return None
    username = json.loads(res.content)["uid"]
    return username        

def statistics_certificates():
    res = session.post("https://mysql:10443/certs_stats", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    res = json.loads(res.content.decode())
    return res["number_certificates"], res["number_revoked"]

def has_valid_certificate(username):
    request_json = {"uid": username}
    res = session.post("https://mysql:10443/all_certs", data=json.dumps(request_json), cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    res = json.loads(res.content.decode())
    if len(res["certificates"])==0:
        return None
    
    return res["certificates"][0]

def add_certificate(username, crt):
    request_json = {"uid": username, "certificate": crt}
    res = session.post("https://mysql:10443/add_user_certificate", data=json.dumps(request_json), cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    return res.status_code

def hash_password(password):
    m = sha1()
    m.update(password.encode())
    return m.hexdigest()

def create_CSR(username):
    # Generate our key
    key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CH"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Zurich"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Zurich"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"iMovies"),
        x509.NameAttribute(NameOID.COMMON_NAME, username),
    ])).sign(key, hashes.SHA256(),backend=default_backend())
    return [key, urlsafe_b64encode(csr.public_bytes(serialization.Encoding.PEM)).decode('utf-8')]

def create_pkcs12(username, key, crt):
    cert = x509.load_pem_x509_certificate(crt.encode())
    pem_pkcs12 = urlsafe_b64encode(serialize_key_and_certificates(name=username.encode('utf-8'), key=key, cert=cert, cas=None, encryption_algorithm=serialization.BestAvailableEncryption(pkcs_12_password.encode()))).decode('utf-8')
    return pem_pkcs12

def save_private_key(username, key):
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    filename = "/backup_dir/" + username + "_" + str(time.time()) + ".pem"
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/core_cert.pem',
                            '/etc/Flask/private/core_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/Flask/certs/cacert.pem')
    with open("/etc/Flask/private/core_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    public_key = private_key.public_key()
    core_server.run(debug=False, ssl_context=context, port=10443, host='0.0.0.0')
