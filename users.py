
import flask
from flask import Flask, request, g, jsonify, Response, json, url_for, make_response
import sqlite3
from cassandra.cluster import Cluster
import hashlib

app = flask.Flask(__name__)
app.config["debug"] = True




@app.route('/auth',methods=['GET'])
def auth():
  	cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    query = "SELECT password FROM users WHERE username = ? AND password = ?"
    if not auth:
        return Response(
            json.dumps({
                'status':   'ERROR',
                'message':  'The operation requires authentication'
            }),
            status='401',
            headers={'WWW-Authenticate': 'Basic realm="Login Required"'},
            mimetype='application/json'
        )
    if not session:
        return Response(Error="Fail to connect to database", status='500')


#User Register
@app.route('/register', methods=['POST'])
def register():
	cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    data = request.get_json()
    user = data['username']
    password = data['password']
    email = data['email']


    #check if user exists
    query = "SELECT username FROM users WHERE username = ?"
    session.execute(query, [user])
    check_user = session.fetchall()
    #if not exist
    if not check_user:
        password_hash = hashlib.md5(password.encode())
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        session.execute(query, [user, email, password_hash.hexdigest()])
        session.commit()
        session.close()
        print(query)
        return jsonify({'Success': 'User Created'}), 201
    else:
        print(query)
        return jsonify({'Error':'User exists'}), 409


@app.route('/users', methods=['DELETE'])
# @auth.required
def delete_user():
	cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    data = request.get_json()
    user = request.authorization['username']
    # password = data['password']
    # password_hash = hashlib.md5(password.encode())
    query = "SELECT username FROM users WHERE username = ?"
    session.execute(query, [user])
    check_user = session.fetchall()
    if check_user:
        query = "DELETE FROM users WHERE username = ?"
        session.execute(query, [user])
        session.commit()
        session.close()
        print(query)
        return jsonify({'Success': 'User deleted'}), 201

@app.route('/users', methods = ['PATCH'])
# @auth.required
def change_pass():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()	
	data = request.get_json()
    user = request.authorization['username']
    new_pass = data['new_pass']
    password_hash = hashlib.md5(new_pass.encode())

  

    query = "SELECT username FROM users WHERE username = ?"
    session.execute(query, [user])
    check_user = session.fetchall()

    if check_user:
        query = "UPDATE users SET password = ? WHERE username = ?"
        session.execute(query, [password_hash.hexdigest(), user])
        session.commit()
        session.close()
        return jsonify({'Success': 'Password changed'}), 201


app.run()
