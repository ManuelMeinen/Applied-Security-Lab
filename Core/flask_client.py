import requests
import sys

from base64 import urlsafe_b64encode, urlsafe_b64decode

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates, load_key_and_certificates
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
######## Authentication cookie ########
# Make a cookie by appending hash256(username+timestamp+randomnumber)
# Save this cookie with filename the cookie and inside put the username
# Put a crontab ereasing cookie if not touch during 10 min
cafile = "/etc/Flask/certs/cacert.pem"
session = requests.Session()
session.verify = cafile

def main():
    username = sys.argv[1]
    [private_key, csr] = create_CSR(username)
    res = session.post("https://ca_server/certs", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'csr': csr})
    if res.status_code != 200:
        print("error")
    else:
        raw_cert = urlsafe_b64decode(res.text.encode('utf-8'))
        cert = x509.load_pem_x509_certificate(raw_cert)
        # print(cert.public_bytes(serialization.Encoding.PEM).decode())
        pem_pkcs12 = urlsafe_b64encode(serialize_key_and_certificates(name=username.encode('utf-8'), key=private_key, cert=cert, cas=None, encryption_algorithm=serialization.NoEncryption())).decode('utf-8')
        f= open("/home/ubuntu/example.p12", "wb")
        f.write(urlsafe_b64decode(pem_pkcs12.encode()))
        f.close()
        f = open("/home/ubuntu/example.pem", "w")
        f.write(cert.public_bytes(serialization.Encoding.PEM).decode())
        f.close()
        raw_cert = urlsafe_b64encode(raw_cert).decode()
        res = session.post("https://ca_server/certs/check", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'crt': raw_cert})
        # print(res.text)
        res = session.delete("https://ca_server/certs", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'crt': raw_cert})
        # print(res.text)
        res = session.post("https://ca_server/certs/check", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'), data={'crt': raw_cert})
        # print(res.text)

    res = session.get("https://ca_server/certs/serial", cert=('/etc/Flask/certs/core_cert.pem', '/etc/Flask/private/core_key.pem'))
    # print(res.text)

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


if __name__== "__main__":
    main()