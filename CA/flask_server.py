from flask import Flask, request
import ssl
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/ca_cert.pem', '/etc/Flask/private/ca_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/ssl/CA/cacert.pem')
    app.run(debug=False, ssl_context=context, port= 443, host= '0.0.0.0')