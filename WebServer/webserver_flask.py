from flask import Flask, send_file, send_from_directory, render_template, request, redirect, session, abort, flash, make_response

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired

import requests
import os
import json
import ssl

from base64 import urlsafe_b64encode, urlsafe_b64decode


app = Flask(__name__)
cafile = "/etc/ssl/certs/cacert.pem"
session = requests.Session()
session.verify = cafile

cert_key = ('/etc/ssl/certs/webserver_cert.pem', '/etc/ssl/private/webserver_key.pem')
MAX_AGE = 60*10

# The cookie name must match the name created by the core server!
userid = 'userID'

UPLOAD_FOLDER = '/var/www/webserver/files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    if not request.cookies.get(userid):
        return render_template('login.html')
    else:
        return render_template('home.html')


@app.route('/login', methods=['POST'])
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
def logout():
    res = make_response(render_template('login.html'))
    res.set_cookie(userid, '', max_age=0)
    return res

class account_form(FlaskForm):
    lastname = StringField("Lastname: ", validators=[DataRequired()])
    firstname = StringField("Firstname: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired()])
    password = StringField('Password', widget=PasswordInput(hide_value=False))
    submit = SubmitField("Submit")

@app.route('/account', methods=['GET', 'POST'])
def account():
    #TODO: this is not secure
    if not request.cookies.get(userid):
        return render_template('login.html')
    if request.method == "GET":
        response = session.get("https://core/account", cookies={'userID': request.cookies.get(userid)}, cert=cert_key)
        if response.status_code == 200:
            data = json.loads(response.content)
            form = account_form()
            return render_template('account.html', form=form, lastname=data['lastname'], firstname=data['firstname'], email=data['email'])
        else:
            return home()
    if request.method == "POST":
        #TODO: check for malicious inputs! 
        data = None
        if request.form['password'] != '':
            data = {"lastname": request.form['lastname'], "firstname": request.form['firstname'], "email": request.form['email'], "password": request.form['password']}
        else :
            data = {"lastname": request.form['lastname'], "firstname": request.form['firstname'], "email": request.form['email']}
        response = session.post("https://core/account", data=data, cert=cert_key, cookies={'userID': request.cookies.get(userid)})
        if response.status_code == 200:
            data = json.loads(response.content)
            form = account_form()
            return render_template('account.html', msg='Your information has been updated', form=form, lastname=data['lastname'], firstname=data['firstname'], email=data['email'])
        else:
            return home()


@app.route('/account/certificate', methods=['POST'])
def account_certificate():
    if not request.cookies.get(userid):
        return render_template('login.html')
    if request.method == "POST":
        response = session.post("https://core/account/certificate", data={}, cert=cert_key, cookies={'userID': request.cookies.get(userid)})
        if (response.status_code == 200):
            #TODO: delete certificate when not needed anymore
            username = json.loads(urlsafe_b64decode(request.cookies.get(userid)).decode())['username']
            filename = username + "_certificate.p12"
            f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb")
            f.write(urlsafe_b64decode(response.content))
            f.close()
            return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)
        if (response.status_code == 400):
            response = session.get("https://core/account/certificate", cert=cert_key, cookies={'userID': request.cookies.get(userid)})
            if response.status_code == 200:
                #TODO: delete certificate when not needed anymore
                username = json.loads(urlsafe_b64decode(request.cookies.get(userid)).decode())['username']
                filename = username + "_certificate.pem"
                f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb")
                f.write(response.content)
                f.close()
                return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)
            else:
                return home()


@app.route('/account/certificate/revocation', methods=['POST'])
def account_certificate_revocation():
    if not request.cookies.get(userid):
        return render_template('login.html')
    response = session.delete("https://core/account/certificate", cert=cert_key, cookies={'userID': request.cookies.get(userid)})
    if response.status_code == 200:
        return render_template('home.html', msg='Your certificate has been revoked.')
    else:
       return render_template('home.html', msg='You do not have a certificate.') 
    

# TODO: check it works when certificate login is working
@app.route('/ca_admin', methods=['get'])
def ca_admin():
    if not request.cookies.get(userid):
        return home()
    response = session.get("https://core/admin", cert=cert_key, cookies={'userID': request.cookies.get(userid)})
    if response.status_code == 200:
        data = json.loads(response.content)
        return render_template('ca_admin.html', serial=data['serial'], nbre_issued=data['nbre_issued'], nbre_revoked=data['nbre_revoked'])
    else:
        return render_template('home.html', error='You are not an admin!')


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


