from flask import Flask, render_template, request, redirect, session, abort, flash
import requests
import os

context=('/etc/ssl/certs/webserver_cert.pem', '/etc/ssl/private/webserver_key.pem')
app = Flask(__name__)
req = requests.Session()

@app.route('/')
def home():
    if not session.get('loggedin'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    data = {"username": request.form['username'], "password": request.form['password'], "crt": ""}
    response = req.post("https://core/login", data=data, cert=context)

    if response.ok:
        session['loggedin'] = True
        session['username'] = request.form['username']
    else:
        flash('Incorrect credentials!')
    return home()

@app.route("/logout")
def logout():
    session['loggedin'] = False
    return home()
   
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(
        debug=False,
        host='192.168.1.20',
        port=443,
        ssl_context=context)

