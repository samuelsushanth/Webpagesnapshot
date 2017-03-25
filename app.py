#!/usr/bin/python
from flask import Flask, jsonify
from flask import request
from flask import abort
from flask import make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask import send_file
import uuid
import MySQLdb
import tarfile
import os
db = MySQLdb.connect("localhost","root","1","coding" )
cursor = db.cursor()
c=db.cursor()
auth = HTTPBasicAuth()
directory=os.getcwd()
@auth.get_password
def get_password(username):
    sql = "SELECT * FROM ACCOUNTS WHERE username = '%s'" % (username)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      uname = row[0]
      paswd = row[1]
      if username == uname:
      	return paswd
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

app = Flask(__name__,static_folder=directory)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'urls' in request.json :
        abort(400)
    uname=auth.username()
    urls = request.json['urls']
    if urls:
    	idee = uuid.uuid4()
    	status='1'	
    	cursor.execute('''INSERT into TASKS (serial,id,username,urls,status) VALUES (NULL,%s,%s,%s,%s)''',(idee,uname,urls,status))
    	db.commit()
    	task={"username":uname,"urls":urls,"id":idee}
    	return jsonify({'task': task}), 201
    else:
    	task={"error":"urls field is empty"}
    	return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    uname=auth.username()
    sql = "SELECT * FROM TASKS WHERE username = '%s'" % (uname)
    cursor.execute(sql)
    results = cursor.fetchall()
    tasks = [{"username":uname}]
    for row in results:
      idee = row[1]
      urls = row[3]
      status = row[4]
      task ={"id":idee,"urls":urls,"status":status}
      tasks.append(task)
    return jsonify({'tasks':tasks})

@app.route('/todo/api/v1.0/tasks/<task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    filename = task_id + '.tar.gz'
#Create Tar file
    tFile = tarfile.open(filename, 'w:gz')
    files = os.listdir(task_id)
    for f in files:
	f = os.path.join(task_id,f)
    	tFile.add(f)
    tFile.close()
#    return send_file(filename, as_attachment=True)
    response = make_response(send_file(filename, as_attachment=True))
    response.headers['X-Something'] = 'header value goes here'
    return response




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/create_account', methods=['POST'])
def create_account():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        abort(400)
    uname = request.json['username']
    paswd = request.json['password']
    sql = "SELECT COUNT(*) FROM ACCOUNTS WHERE username = '%s'" % (uname)
    cursor.execute(sql)
    db.commit()
    (number_of_rows,)=cursor.fetchone()
    if number_of_rows != 0:
    	task={"message":"choose a different username"}
    	return jsonify({'task': task}), 201
    else :
    	cursor.execute('''INSERT into ACCOUNTS (username,password) VALUES (%s, %s)''',(uname,paswd))
    	db.commit()
    	task={"username":uname,"password":paswd,"message":"success"}
    	return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(debug=True)
