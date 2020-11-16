import sql_server
import json
from flask import Flask, request
import ssl


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to MySQL server!'


@app.route('/password', methods=['POST'])
def get_password():
    '''
    return user's hashed password as json {"pwd":"hashed_pwd"}, if not found then hashed_pwd=empty string
    post a json request with user's uid in the json
    '''
    if not is_json(request.data):
        return "Not valid JSON as input", 400

    data = json.loads(request.data)

    if 'uid' not in data:
        return "Missing the uid parameter",400

    uid = data['uid']
    response = sql_server.get_password(uid)


    if response is None:
        return "Password not found", 404
    
    json_response = '{"pwd":"'+response[0]+'"}'

    return json_response

@app.route('/get_info', methods=['POST'])
def get_info():

    if not is_json(request.data):
        return "Not valid JSON as input", 400

    data = json.loads(request.data)


    if 'uid' not in data:
        return "Missing the uid parameter",400

    uid = data['uid']

    user_info_list = sql_server.get_user_info(uid)

    user_is_admin = sql_server.get_admin_info(uid)

    if user_info_list is None:
        return "users infos not found", 404

    if user_is_admin is None:
        user_is_admin = 'false'
    elif user_is_admin[0]==1:
        user_is_admin = 'true'
    else:
        user_is_admin = 'false'
    
    json_response = '{"lastname":"'+user_info_list[0]+'", "firstname":"'+user_info_list[1]+'", "mail":"'+user_info_list[2]+'"}'

    return json_response


@app.route('/update', methods=['POST'])
def update_info():
    '''
    needs the uid string in the post request, as well as the fields that will be updated
    return the updated json
    '''
    if not is_json(request.data):
        return "Not valid JSON as input", 400

    data = json.loads(request.data)


    if 'uid' not in data:
        return "Missing the uid parameter",400

    uid = data['uid']

    #returns lastname, firstname, mail
    user_info_list = sql_server.get_user_info(uid)
    #pwd
    user_pwd = sql_server.get_password(uid)
    #is_admin
    user_is_admin = sql_server.get_admin_info(uid)

    if user_info_list is None:
        return "no user found", 404
    
    lastname = user_info_list[0]
    if 'lastname' in data:
        lastname = data['lastname']
    
    firstname = user_info_list[1]
    if 'firstname' in data:
        firstname = data['firstname']
    
    mail = user_info_list[2]
    if 'mail' in data:
        mail = data['mail']

    password = user_pwd[0]
    if 'pwd' in data:
        password = data['pwd']

    is_admin = user_is_admin[0]
    if 'is_admin' in data:
        is_admin = data['is_admin']

    
    user_new_info_list = sql_server.update_user_data(uid, lastname, firstname, mail, password, is_admin)

    user_info_list = sql_server.get_user_info(uid)

    user_is_admin = sql_server.get_admin_info(uid)

    if user_info_list is None:
        return "We got a problem, sorry user not updated", 520

    if user_is_admin is None:
        user_is_admin = 'false'
    elif user_is_admin[0]==1:
        user_is_admin = 'true'
    else:
        user_is_admin = 'false'

    password = sql_server.get_password(uid)[0]
    
    json_response = '{"lastname":"'+user_info_list[0]+'", "firstname":"'+user_info_list[1]+'", "mail":"'+user_info_list[2]+'", "pwd":"'+password+'", "is_admin":'+user_is_admin+'}'

    return json_response


@app.route('/add_user', methods=['POST'])
def add_user():

    '''
    needs full json, if uid or pwd not present, nothing would be added, everything else is replaced by default values if absent
    '''

    if not is_json(request.data):
        return "Not valid JSON as input", 400

    data = json.loads(request.data)

    if ('uid' not in data) or ('pwd' not in data):
        return "Missing the uid or pwd parameter",400
    
    uid= data['uid']
    password = data['pwd']
    lastname=''
    firstname=''
    mail=''
    is_admin = 0

    if 'lastname' in data:
        lastname=data['lastname']

    if 'firstname' in data:
        firstname = data['firstname']
    
    if 'mail' in data:
        mail = data['mail']
    
    if 'is_admin' in data:
        if data['is_admin']:
            is_admin=1
        else:
            is_admin=0
    

    new_user_info = sql_server.add_user(uid, lastname, firstname, mail, password, is_admin)


    return ":)", 200

@app.route('/add_user_certificate', methods=['POST'])
def add_certificate():
    if not is_json(request.data):
        return "Not valid JSON as input", 400

    data = json.loads(request.data)

    if ('uid' not in data) or ('certificate' not in data):
        return "Missing the uid or certificate parameter",400

    uid = data['uid']

    certificate = ''
    if 'certificate' in data:
        certificate=data['certificate']
    print(certificate)
    added_row = sql_server.add_certificate(uid, certificate)

    if added_row is None:
        return "Something went wrong, sorry", 520

    return ":)", 200

@app.route('/revoke_user_certificate', methods=['POST'])
def revoke_certificate():

    if not is_json(request.data):
        return "Not valid JSON as input", 400

    data = json.loads(request.data)


    if 'certificate' not in data:
        return "Missing the certificate parameter",400

    certificate = data['certificate']

    deleted_cert = sql_server.delete_certificate(certificate)


    if deleted_cert:
        return ":)", 200
    else:
        return "the certificate was not revoked :(", 520

    return "the certificate was not revoked :(", 520


@app.route('/who_has_this_cert', methods=['POST'])
def get_uid_from_cert():

    if not is_json(request.data):
        return "Not valid JSON as input", 400    

    data = json.loads(request.data)

    if 'certificate' not in data:
        return "Missing the certificate parameter",400

    certificate = data['certificate']

    uid = sql_server.get_uid_from_cert(certificate)

    if uid is None:
        return "No uid found :( ", 404
    
    return '{"uid": "'+uid[0]+'"}'


@app.route('/all_certs', methods=['POST'])
def get_all_certs():

    if not is_json(request.data):
        return "Not valid JSON as input", 400

    data = json.loads(request.data)

    if 'uid' not in data:
        return "Missing the uid parameter",400

    uid = data['uid']

    certs = sql_server.get_certs(uid)

    if not certs:
        return '{"certificates": []}'

    certs = [e[0] for e in certs]

    string_certs = '['
    for c in certs:
        string_certs = string_certs + '"'+ c+ '"'+','
    string_certs = string_certs[:-1] if string_certs[-1] == ',' else string_certs
    string_certs = string_certs + ']'

    print("STRING CERTS", string_certs)

    response_json = '{"certificates": '+string_certs+'}'

    return response_json


@app.route('/certs_stats', methods=['POST'])
def get_stats():

    stats = sql_server.get_stats()
    n_certs, n_revoked = stats[0]

    if n_revoked is None:
        n_revoked = 0
    else:
        n_revoked = int(n_revoked)

    return '{"number_certificates":'+str(n_certs)+',"number_revoked":'+str(n_revoked)+'}'


def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True



if __name__ == '__main__':

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/mysql_cert.pem',
                            '/etc/Flask/private/mysql_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/Flask/certs/cacert.pem')
    app.run(debug=False, ssl_context=context, port=443, host='0.0.0.0')
