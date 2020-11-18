from flask import Flask, request, make_response
from cryptography.hazmat.primitives import serialization

import os
import ssl
core_server = Flask(__name__)


@core_server.route("/")
def home():
    return str(request.headers['X-SSL-CERT'])

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/core_cert.pem',
                            '/etc/Flask/private/core_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/Flask/certs/cacert.pem')
    core_server.run(debug=False, ssl_context=context, port=10443, host='0.0.0.0')
