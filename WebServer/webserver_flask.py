from flask import Flask, send_file, send_from_directory, render_template, request, redirect, session, abort, flash, make_response
import requests
import os
import json
import ssl


app = Flask(__name__)
cafile = "/etc/ssl/certs/cacert.pem"
session = requests.Session()
session.verify = cafile

cert_key = ('/etc/ssl/certs/webserver_cert.pem', '/etc/ssl/private/webserver_key.pem')

# The cookie name must match the name created by the core server!
userid = 'userID'


@app.route('/')
def home():
    if not request.cookies.get(userid):
        return render_template('login.html')
    else:
        return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    data = {"username": request.form['username'], "password": request.form['password']}
    response = None
    try:
        response = session.post("https://core/login", data=data, cert=cert_key)
    except requests.exceptions.ConnectionError:
        flash('Connection refused!')
        return home()

    #print response
    print(response)
    if response != None and response.ok:
        res = make_response(render_template('home.html'))
        res.set_cookie(userid, response.cookies, max_age=60*10)
        return res
    else:
        flash('Incorrect credentials!')
        return home()


@app.route("/logout", methods=['POST'])
def logout():
    res = make_response(render_template('login.html'))
    res.set_cookie(userid, '', max_age=0)
    return res

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain('/etc/ssl/certs/webserver_cert.pem',
                            '/etc/ssl/private/webserver_key.pem')
    context.verify_mode = ssl.CERT_OPTIONAL
    context.load_verify_locations('/etc/ssl/certs/cacert.pem')
    app.secret_key = os.urandom(12)
    app.run(
        debug=False,
        host='192.168.1.20',
        port=443,
        ssl_context=context)
