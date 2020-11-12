from flask import Flask, render_template, redirect
from threading import Thread
import os

#redirection
redirect = Flask('redirect')
@redirect.route('/')
def index():
    #return redirect('https://192.168.1.20', 301)
    return 'success'


#webserver
context=('/media/asl/WebServer/webserver_cert.pem', '/media/asl/WebServer/webserver_key.pem')
webserver = Flask('webserver')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(
        debug=False,
        host='192.168.1.20',
        port=443, 
        ssl_context=context)
