from flask import Flask, render_template, request, redirect, session, abort, flash, make_response
import requests
import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


context=('/etc/ssl/certs/webserver_cert.pem', '/etc/ssl/private/webserver_key.pem')
app = Flask(__name__)
session = requests.Session()

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
    # data = {"username": request.form['username'], "password": request.form['password'], "crt": ""}
    # response = None
    # try:
    #     response = session.post("https://core/login", data=data, cert=context)
    # except requests.exceptions.ConnectionError:
    #     flash('Connection refused!')
    #     return home()

    # if response != None and response.ok:
    #     res = make_response(render_template('home.html'))
    #     res.set_cookie(userid, response.cookies, max_age=60*10)
    #     return res
    # else:
    #     flash('Incorrect credentials!')
    # return home()


    #
    # Local code
    #
    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
        cookie = {
            "username": request.form['username'],
            "timestamp": 0,
            "nonce": 0,
            "signature": 0
        }
        cookie = urlsafe_b64encode(json.dumps(cookie).encode()).decode()
        res = make_response(render_template('home.html'))
        res.set_cookie(userid, cookie, max_age=60*10)
        return res
    else:
        flash ('Incorrect credentials!')
    return home()


class cert_issuance_show_info_form(FlaskForm):
    lastname = StringField("Lastname: ", validators=[DataRequired()])
    firstname = StringField("Firstname: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    submit = SubmitField("Submit")

@app.route('/cert_issuance/show_info', methods=['GET'])
def cert_issuance_show_info():
    # response = None
    # try:
    #     response = session.get("https://core/account", cookies=request.cookies.get(userid), cert=context)
    # except requests.exceptions.ConnectionError:
    #     flash('Connection refused!')
    #     return home()

    # if response != None and response.ok:
    #     # todo
    #     return render_template('cert_issuance.html')
    # else:
    #     flash('An error occurs!')
    #     return home() 


    #
    # Local code
    #
    if request.cookies.get(userid):
        form = cert_issuance_show_info_form()
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('cert_issuance_show_info.html', form=form, lastname="Jean-Bernard", firstname="Petolet", email="jb.petolet@asl.ch")
        return render_template('cert_issuance_show_info.html', form=form, lastname="Jean-Bernard", firstname="Petolet", email="jb.petolet@asl.ch")
    else:
        flash('An error occurs!')
        return home() 

@app.route('/cert_issuance/issue', methods=['post'])
def cert_issuance_issue():
    return render_template('cert_issuance_download_cert.html')

@app.route("/logout", methods=['POST'])
def logout():
    res = make_response(render_template('login.html'))
    res.set_cookie(userid, '', max_age=0)
    return res

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(
        debug=False,
        host='192.168.1.20',
        port=443,
        ssl_context=context)

