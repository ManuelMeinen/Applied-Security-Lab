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
    data = json.loads(request.data)
    uid = data['uid']
    response = sql_server.get_password(uid)

    if response is None:
        return '{"pwd": ""}'
    
    json_response = '{"pwd":"'+response[0]+'"}'

    return json_response

@app.route('/get_info', methods=['POST'])
def get_info():
    '''
    return user's info (lastname, firstname, mail, is_admin), as json string, 
    if not found then empty json
    post a json request with user's uid in the json
    '''
    data = json.loads(request.data)
    uid = data['uid']

    user_info_list = sql_server.get_user_info(uid)

    if user_info_list is None:
        user_info_list=['', '', '', '']
    
    is_admin = 0
    if user_info_list[3]==1:
        is_admin='true'
    else:
        is_admin='false'

    
    json_response = '{"lastname":"'+user_info_list[0]+'", "firstname":"'+user_info_list[1]+'", "mail":"'+user_info_list[2]+'", "is_admin":'+is_admin+'}'

    return json_response


@app.route('/update', methods=['POST'])
def update_info():
    '''
    needs the uid string in the post request, as well as the fields that will be updated
    return the updated json
    '''
    data = json.loads(request.data)
    uid = data['uid']

    user_info_list = sql_server.get_user_info(uid)

    if user_info_list is None:
        return '{"lastname":"", "firstname":"", "mail":"", "is_admin":false}'
    
    lastname = user_info_list[0]
    if 'lastname' in data:
        lastname = data['lastname']
    
    firstname = user_info_list[1]
    if 'firstname' in data:
        firstname = data['firstname']
    
    mail = user_info_list[2]
    if 'mail' in data:
        mail = data['mail']
    
    is_admin = user_info_list[3]
    if 'is_admin' in data:
        if data['is_admin']:
            is_admin=1
        else:
            is_admin=0
    
    user_new_info_list = sql_server.update_user_data(uid, lastname, firstname, mail, is_admin)

    is_admin = 0
    if user_new_info_list[3]==1:
        is_admin='true'
    else:
        is_admin='false'

    json_response = '{"lastname":"'+user_new_info_list[0]+'", "firstname":"'+user_new_info_list[1]+'", "mail":"'+user_new_info_list[2]+'", "is_admin":'+is_admin+'}'

    return json_response


@app.route('/add_user', methods=['POST'])
def add_user():

    '''
    needs full json, if uid or pwd not present, nothing would be added, everything else is replaced by default values if absent
    '''
    data = json.loads(request.data)

    if ('uid' not in data) or ('pwd' not in data):
        return '{"lastname":"", "firstname":"", "mail":"", "is_admin":false}'
    
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

    if new_user_info is None:
        return '{"lastname":"", "firstname":"", "mail":"", "is_admin":false}'
    
    is_admin = 0
    if new_user_info[3]==1:
        is_admin='true'
    else:
        is_admin='false'

    
    json_response = '{"lastname":"'+new_user_info[0]+'", "firstname":"'+new_user_info[1]+'", "mail":"'+new_user_info[2]+'", "is_admin":'+is_admin+'}'

    return json_response

@app.route('/delete_user', methods=['POST'])
def delete_user():
    '''
    with the uid, delete everything from users_info and users_certificates tables
    return json deleted=0 if everything okay, else:deleted=1 
    '''
    
    data = json.loads(request.data)
    uid = data['uid']

    user_deleted = sql_server.delete_user(uid)

    if user_deleted:
        return '{"deleted": 0}'
    else:
        return '{"deleted": 1}'

    return '{"deleted": 1}'

@app.route('/add_user_certificate', methods=['POST'])
def add_certificate():
    data = json.loads(request.data)
    uid = data['uid']

    certificate = ''
    if 'certificate' in data:
        certificate=data['certificate']

    added_row = sql_server.add_certificate(uid, certificate)

    if added_row is None:
        return '{"uid":"", "certificate": ""}'

    json_response = '{"uid":"'+added_row[0]+'", "certificate": "'+added_row[1]+'"}'

    return json_response

@app.route('/delete_user_certificate', methods=['POST'])
def delete_certificate():
    data = json.loads(request.data)
    certificate = data['certificate']

    deleted_cert = sql_server.delete_certificate(certificate)

    if deleted_cert:
        return '{"deleted": 0}'
    else:
        return '{"deleted": 1}'

    return '{"deleted": 1}'


@app.route('/who_has_this_cert', methods=['POST'])
def get_uid_from_cert():
    data = json.loads(request.data)
    certificate = data['certificate']

    uid = sql_server.get_uid_from_cert(certificate)

    if uid is None:
        return '{"uid": ""}'
    
    return '{"uid": "'+uid[0]+'"}'


@app.route('/all_certs', methods=['POST'])
def get_all_certs():
    data = json.loads(request.data)
    uid = data['uid']

    certs = sql_server.get_certs(uid)

    if certs is None:
        return '{"certificates": []}'

    certs = [e[0] for e in certs]

    string_certs = '['
    for c in certs:
        string_certs = string_certs + '"'+ c+ '"'+','
    string_certs = string_certs[:-1]
    string_certs = string_certs + ']'

    print("STRING CERTS", string_certs)

    response_json = '{"certificates": '+string_certs+'}'

    return response_json




if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/Flask/certs/mysql_cert.pem',
                            '/etc/Flask/private/mysql_key.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/Flask/certs/cacert.pem')
    app.run(debug=False, ssl_context=context, port=443, host='0.0.0.0')