from flask import Flask, send_file, send_from_directory, render_template, request, redirect, session, abort, flash, make_response
from base64 import urlsafe_b64encode, urlsafe_b64decode
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
import requests
import os
import json
import ssl


app = Flask(__name__)
cafile = "/etc/ssl/certs/cacert.pem"
session = requests.Session()
session.verify = cafile

context = ('/etc/ssl/certs/webserver_cert.pem', '/etc/ssl/private/webserver_key.pem')

# The cookie name must match the name created by the core server!
userid = 'userID'

# Remove ?
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
    data = {"username": request.form['username'], "password": request.form['password']}
    response = None
    try:
        response = session.post("https://core/login", cert=('/etc/ssl/certs/webserver_cert.pem',
                                                   '/etc/ssl/private/webserver_key.pem'), data={'username': "admin", "password": "KK38O!M=HiCC20g9mS_gFgC"})
        #response = session.post("https://core/login", data=data, cert=context)
    except requests.exceptions.ConnectionError:
        flash('Connection refused!')
        return home()

    if response != None and response.ok:
        res = make_response(render_template('home.html'))
        res.set_cookie(userid, response.cookies, max_age=60*10)
        return res
    else:
        flash('Incorrect credentials!')
        return home()


    #
    # Local code
    #
    # if request.form['username'] == 'admin' and request.form['password'] == 'admin':
    #     cookie = {
    #         "username": request.form['username'],
    #         "timestamp": 0,
    #         "nonce": 0,
    #         "signature": 0
    #     }
    #     cookie = urlsafe_b64encode(json.dumps(cookie).encode()).decode()
    #     res = make_response(render_template('home.html'))
    #     res.set_cookie(userid, cookie, max_age=60*10)
    #     return res
    # else:
    #     flash ('Incorrect credentials!')
    #     return home()


@app.route('/login_with_cert', methods=['POST'])
def login_with_cert():
    # if 'file' not in request.files:
    #     flash ('No file')
    #     return home()
    # file = request.files['file']
    # if file.filename == '':
    #     flash('No filename')
    #     return home()
    # if file:
    #     response = None
    #     try:
    #         response = session.post("https://core/login", data=request.files, cert=context)
    #     except requests.exceptions.ConnectionError:
    #         flash('Connection refused!')
    #         return home()

    #     if response != None and response.ok:
    #         res = make_response(render_template('home.html'))
    #         res.set_cookie(userid, response.cookies, max_age=60*10)
    #         return res
    # else:
    #     flash('Incorrect credentials!')
    # return home()


    #
    # Local code
    #  
    if 'file' not in request.files:
        flash ('No file')
        return home()
    file = request.files['file']
    if file.filename == '':
        flash('No filename')
        return home()
    if file:
        cookie = {
            "username": "admin",
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
    email = StringField("Email: ", validators=[DataRequired()])
    password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/cert_issuance/show_info', methods=['GET'])
def cert_issuance_show_info():
    # if not request.cookies.get(userid):
    #     return render_template('login.html')
    # response = None
    # try:
    #     response = session.get("https://core/account", cookies=request.cookies.get(userid), cert=context)
    # except requests.exceptions.ConnectionError:
    #     flash('Connection refused!')
    #     return home()

    # if response != None and response.ok:
    #     data = json.loads(response.content)
    #     form = cert_issuance_show_info_form()
    #     return render_template('cert_issuance_show_info.html', form=form, lastname=data['lastname'], firstname=data['firstname'], email=data['email'], password=data['password'])
    # else:
    #     flash('An error occurs!')
    #     return home() 


    #
    # Local code
    #
    if not request.cookies.get(userid):
        return render_template('login.html')
    if request.cookies.get(userid):
        form = cert_issuance_show_info_form()
        return render_template('cert_issuance_show_info.html', form=form, lastname="Jean-Bernard", firstname="Petolet", email="jb.petolet@asl.ch", password="1234")
    else:
        flash('An error occurs!')
        return home() 

@app.route('/cert_issuance/update_info', methods=['POST'])
def cert_issuance_update_info():
    #TODO: check inputs form! 
    # if not request.cookies.get(userid):
    #     return render_template('login.html')
    # data = {"lastname": request.form['lastname'], "firstname": request.form['firstname'], "email": request.form['email'], "password": request.form['password']}
    # response = None
    # try:
    #     response = session.post("https://core/account", data=data, cert=context, cookies=request.cookies.get(userid),)
    # except requests.exceptions.ConnectionError:
    #     flash('Connection refused!')
    #     return home()

    # if response != None and response.ok:
    #     flash("Information have been updated.")    
    #     return redirect("https://webserver/cert_issuance/show_info")
    # else:
    #     flash('An error occurs!')
    #     return home()


    #
    # Local code
    #
    if not request.cookies.get(userid):
        return render_template('login.html')
    flash("Information have been updated.")    
    return redirect("https://webserver/cert_issuance/show_info")

@app.route('/cert_issuance/issue', methods=['get'])
def cert_issuance_issue():
    # if not request.cookies.get(userid):
    #     return render_template('login.html')
    # response = None
    # try:
    #     response = session.post("https://core/account/certificate", cert=context, cookies=request.cookies.get(userid),)
    # except requests.exceptions.ConnectionError:
    #     flash('Connection refused!')
    #     return home()

    # if response != None and response.ok:
    #     response.content.save(os.path.join(app.config['UPLOAD_FOLDER'], "certificate"))
    #     flash("Get your certificate.")    
    #     return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename="certificate", as_attachment=True)
    # else:
    #     flash('An error occurs!')
    #     return home()


    #
    # Local code
    #    
    if not request.cookies.get(userid):
        return render_template('login.html')
    flash('Get your certificate.')
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename="certificate_test.pem", as_attachment=True)


@app.route('/cert_revocation', methods=['post'])
def cert_revocation():
    # if not request.cookies.get(userid):
    #     return render_template('login.html')
    # response = None
    # try:
    #     response = session.delete("https://core/account/certificate", cert=context, cookies=request.cookies.get(userid))
    # except requests.exceptions.ConnectionError:
    #     flash('Connection refused!')
    #     return home()

    # if response != None and response.ok:
    #     flash("Certificate revoked.")    
    #     return home()
    # else:
    #     flash('An error occurs!')
    #     return home()


    #
    # Local code
    #  
    if not request.cookies.get(userid):
        return render_template('login.html')
    flash("Certificate revoked.")    
    return home()


@app.route('/ca_admin', methods=['get'])
def ca_admin():
    # if not request.cookies.get(userid):
    #     return render_template('login.html')
    # response = None
    # try:
    #     response = session.get("https://core/admin", cert=context, cookies=request.cookies.get(userid))
    # except requests.exceptions.ConnectionError:
    #     flash('Connection refused!')
    #     return home()

    # if response != None and response.ok:
    #     data = json.loads(response.content)
    #     return render_template('ca_admin.html', serial=data['serial'], nbre_issued=data['nbre_issued'], nbre_revoked=data['nbre_revoked'])
    # else:
    #     flash('An error occurs!')
    #     return home()


    #
    # Local code
    #
    if not request.cookies.get(userid):
        return render_template('login.html')
    if request.cookies.get(userid):
        return render_template('ca_admin.html', serial="a86saf97sf9", nbre_issued="42", nbre_revoked="13")
    else:
        flash('An error occurs!')
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
    # app.secret_key = os.urandom(12)
    app.run(
        debug=False,
        host='192.168.1.20',
        port=443,
        ssl_context=context)


