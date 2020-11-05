from flask import Flask, request, make_response
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import subprocess
import uuid
import json
import time
import os
import ssl
core_server = Flask(__name__)
private_key = None
public_key = None
@core_server.route("/login", methods=["POST"])
def login():
    # Cookie is JSON with username, timestamp, nonce, signed hash of the three information => base64
    username = request.form['username']
    timestamp = str(time.time())
    nonce = str(uuid.uuid4().hex)
    message = username + timestamp + nonce
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
        "username" : username,
        "timestamp" : timestamp,
        "nonce": nonce,
        "signature": urlsafe_b64encode(signature).decode()
    }
    cookie = urlsafe_b64encode(json.dumps(cookie).encode()).decode()
    res = make_response("Hello " + username)
    res.set_cookie("userID", cookie, max_age=60*20)
    return res

@core_server.route("/admin", methods=["GET"])
def admin():
    if check_cookie(request):
        stat = {
            "serial"  :  "01",
            "nbreissued" :10,    
            "nbrerevoked": 5}
        return json.dumps(stat)
    else:
        return "Authentication Failed", 403

@core_server.route("/admin/newuser", methods=["POST"])
def add_new_user():
    if check_cookie(request):
        username = request.form["username"]
        password = request.form["password"]
        is_admin = request.form["is_admin"]
        if username == None or password == None or not (is_admin == "true" or is_admin == "false"):
            return "Some fields are missing", 400
        response = {
            "username": username,
            "is_admin": is_admin
        }
        return json.dumps(response)
    return "Authentication Failed", 403
def check_cookie(request):
    try:
        cookie = request.cookies.get("userID")
        cookie = json.loads(urlsafe_b64decode(cookie.encode()).decode())
        username = cookie["username"]
        timestamp = cookie["timestamp"] 
        nonce = cookie["nonce"] 
        signature = urlsafe_b64decode(cookie["signature"].encode())
        message = username + timestamp + nonce
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
    except:
        return False

    return True

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/Flask/certs/cacert.pem')
    with open("/etc/Flask/private/core_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )
    public_key = private_key.public_key()
    core_server.run(debug=False, ssl_context=context, port= 443, host= '0.0.0.0')