from flask import Flask, send_file, render_template, request, redirect, session, abort, flash, make_response
from flask_behind_proxy import FlaskBehindProxy

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

import requests
import os
import json
import ssl
import time
import re 

from base64 import urlsafe_b64encode, urlsafe_b64decode


app = Flask(__name__)
app_proxied = FlaskBehindProxy(app)
cafile = "/etc/ssl/certs/cacert.pem"
session = requests.Session()
session.verify = cafile

cert_key = ('/etc/ssl/certs/webserver_cert.pem', '/etc/ssl/private/webserver_key.pem')
MAX_AGE = 60*10

# The cookie name must match the name created by the core server!
userid = 'userID'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/')
@limiter.exempt
def home():
    if is_loggedin():
        return render_template('home.html')
    else:
        if request.headers.get('X-SSL-Client-Cert'):
            data = {'crt': request.headers['X-SSL-Client-Cert']}
            print(data)
            response = session.post("https://core/login", data=data, cert=cert_key)
            print(response)
            if response.status_code == 200:
                res = make_response(render_template('home.html'))
                res.set_cookie(userid, response.cookies.get('userID'), max_age=MAX_AGE)
                return res
            else:
                return render_template('login.html', msg='Unknown certificate!')
        return render_template('login.html')


@app.route('/login', methods=['POST'])
@limiter.limit("5/minute")
def login():
    if request.method == "POST":
        data = {"username": request.form['username'], "password": request.form['password']}
        response = session.post("https://core/login", data=data, cert=cert_key)
        if response.status_code == 200:
            res = make_response(render_template('home.html'))
            res.set_cookie(userid, response.cookies.get('userID'), max_age=MAX_AGE)
            return res
        else:
            return render_template('login.html', msg='Wrong credentials!')
    else:
        home()


@app.route("/logout", methods=['POST'])
@limiter.exempt
def logout():
    res = make_response(render_template('login.html'))
    res.set_cookie(userid, '', max_age=0)
    return res


class account_form(FlaskForm):
    lastname = StringField("Lastname: ", validators=[DataRequired(), Length(max=15)])
    firstname = StringField("Firstname: ", validators=[DataRequired(), Length(max=15)])
    email = StringField("Email: ", validators=[Email(), Length(max=30)])
    password = PasswordField('Password')
    submit = SubmitField("Submit")

@app.route('/account', methods=['GET', 'POST'])
@limiter.exempt
def account():
    if not is_loggedin():
        return home()
    if request.method == "GET":
        response = session.get("https://core/account", cookies={'userID': request.cookies.get(userid)}, cert=cert_key)
        if response.status_code == 200:
            data = json.loads(response.content)
            form = account_form()
            return render_template('account.html', form=form, lastname=data['lastname'], firstname=data['firstname'], email=data['email'])
        else:
            return home()
    if request.method == "POST":
        form = account_form()
        form.firstname(value=request.form['firstname'])
        form.lastname(value=request.form['lastname'])
        form.email(value=request.form['email'])
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        regex_email = re.compile('[_!#$%^&*()<>?/\|}{~:]')
        if form.validate() and regex.search(request.form['firstname']) == None and regex.search(request.form['lastname']) == None and regex_email.search(request.form['email']) == None:
            data = None
            if request.form['password'] != '':
                data = {"lastname": request.form['lastname'], "firstname": request.form['firstname'], "email": request.form['email'], "password": request.form['password']}
            else :
                data = {"lastname": request.form['lastname'], "firstname": request.form['firstname'], "email": request.form['email']}
            response = session.post("https://core/account", data=data, cert=cert_key, cookies={'userID': request.cookies.get(userid)})
            if response.status_code == 200:
                data = json.loads(response.content)
                return render_template('account.html', msg='Your information has been updated', form=form, lastname=data['lastname'], firstname=data['firstname'], email=data['email'])
            else:
                return home()
        return render_template('account.html', msg='The inputs are not correct', form=form, lastname=request.form['lastname'], firstname=request.form['firstname'], email=request.form['email'])


@app.route('/account/certificate', methods=['POST'])
@limiter.exempt
def account_certificate():
    if not is_loggedin():
        return home()
    if request.method == "POST":
        response = session.post("https://core/account/certificate", data={}, cert=cert_key, cookies={'userID': request.cookies.get(userid)})
        if (response.status_code == 200):
            username = json.loads(urlsafe_b64decode(request.cookies.get(userid)).decode())['username']
            filename = username + "_certificate.p12"
            response = make_response(urlsafe_b64decode(response.content))
            response.headers.set('Content-Type', 'application/octet-stream')
            response.headers.set('Content-Disposition', 'attachment', filename=filename)
            return response
        if (response.status_code == 400):
            response = session.get("https://core/account/certificate", cert=cert_key, cookies={'userID': request.cookies.get(userid)})
            if response.status_code == 200:
                username = json.loads(urlsafe_b64decode(request.cookies.get(userid)).decode())['username']
                filename = username + "_certificate.pem"
                response = make_response(response.content)
                response.headers.set('Content-Type', 'application/text')
                response.headers.set('Content-Disposition', 'attachment', filename=filename)
                return response
            else:
                return home()


@app.route('/account/certificate/revocation', methods=['POST'])
@limiter.exempt
def account_certificate_revocation():
    if not is_loggedin():
        return home()
    response = session.delete("https://core/account/certificate", cert=cert_key, cookies={'userID': request.cookies.get(userid)})
    if response.status_code == 200:
        return render_template('home.html', msg='Your certificate has been revoked.')
    else:
       return render_template('home.html', msg='You do not have a certificate.') 
    
    
@app.route('/revocation_list', methods=['GET'])
@limiter.exempt
def revocation_list():
    revoked = session.get("https://core/revocation_list", data={}, cert=cert_key)
    filename = "revocation_list.crl"
    response = make_response(revoked.content)
    response.headers.set('Content-Type', 'application/text')
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response
    

# TODO: check it works when certificate login is working
@app.route('/ca_admin', methods=['get'])
@limiter.exempt
def ca_admin():
    if not is_loggedin():
        return home()
    response = session.get("https://core/admin", cert=cert_key, cookies={'userID': request.cookies.get(userid)})
    if response.status_code == 200:
        data = json.loads(response.content)
        return render_template('ca_admin.html', serial=data['serial'], nbre_issued=data['nbreissued'], nbre_revoked=data['nbrerevoked'])
    else:
        return render_template('home.html', msg='You are not an admin.')


def is_loggedin():
    if request.cookies.get("userID"):
        cookie = request.cookies.get("userID")
        cookie = json.loads(urlsafe_b64decode(cookie.encode()).decode())
        timestamp = cookie["timestamp"]
        if(time.time() - float(timestamp) > MAX_AGE):
            return False
        else:
            return True
    else:
        return False


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain('/etc/ssl/certs/webserver_cert.pem',
                            '/etc/ssl/private/webserver_key.pem')
    context.verify_mode = ssl.CERT_OPTIONAL
    context.load_verify_locations('/etc/ssl/certs/cacert.pem')
    app.secret_key = os.urandom(12)
    app.run(
        debug=False,
        host='127.0.0.1',
        port=8081,
        ssl_context=context)


