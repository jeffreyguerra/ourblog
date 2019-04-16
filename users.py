
import flask
from flask import Flask, request, g, jsonify, Response, json, url_for, make_response
import sqlite3
# from flask_basicauth import BasicAuth
import hashlib

app = flask.Flask(__name__)
app.config["debug"] = True
DATABASE = "user.db"

# class bAuth(BasicAuth):
#     def check_credentials(self, username, password):
#         conn = sqlite3.connect(DATABASE)
#         cur = conn.cursor()
#         password_hash = hashlib.md5(password.encode())
#         query = "SELECT * FROM users WHERE username = ? AND password = ?"
#         cur.execute(query, [username, password_hash.hexdigest()])
#         result = cur.fetchall()
#         conn.close()
#         if result:
#             return True
#         else:
#             return False
#
# auth = bAuth(app)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/auth',methods=['GET'])
def auth():
    auth = request.authorization
    conn = sqlite3.connect(DATABASE)
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
    if not conn:
        return Response(Error="Fail to connect to database", status='500')
    c = conn.cursor()
    try:
        c.execute(query)
        result = c.fetchone()
    except:
        return Response(Error="Error running query to database", status='500')

    if not result or len(result) == 0:
        return Response(
            json.dumps({
                'status':   'ERROR',
                'message':  'The provided credentials are incorrect'
            }),
            status='401',
            mimetype='application/json'
        )
    else:
        return Response(
            json.dumps({
                'status': 'OK',
            }),
            status='200',
            mimetype='application/json'
        )

#User Register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = data['username']
    password = data['password']
    email = data['email']
    conn = sqlite3.connect(DATABASE)
    #conn.row_factory = make_dicts
    cur = conn.cursor()

    #check if user exists
    query = "SELECT username FROM users WHERE username = ?"
    cur.execute(query, [user])
    check_user = cur.fetchall()
    #if not exist
    if not check_user:
        password_hash = hashlib.md5(password.encode())
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        cur.execute(query, [user, email, password_hash.hexdigest()])
        conn.commit()
        conn.close()
        print(query)
        return jsonify({'Success': 'User Created'}), 201
    else:
        print(query)
        return jsonify({'Error':'User exists'}), 409


@app.route('/users', methods=['DELETE'])
# @auth.required
def delete_user():
    data = request.get_json()
    user = request.authorization['username']
    # password = data['password']
    # password_hash = hashlib.md5(password.encode())

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    cur = conn.cursor()
    query = "SELECT username FROM users WHERE username = ?"
    cur.execute(query, [user])
    check_user = cur.fetchall()
    if check_user:
        query = "DELETE FROM users WHERE username = ?"
        cur.execute(query, [user])
        conn.commit()
        conn.close()
        print(query)
        return jsonify({'Success': 'User deleted'}), 201

@app.route('/users', methods = ['PATCH'])
# @auth.required
def change_pass():
    data = request.get_json()
    user = request.authorization['username']
    new_pass = data['new_pass']
    password_hash = hashlib.md5(new_pass.encode())

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    cur = conn.cursor()

    query = "SELECT username FROM users WHERE username = ?"
    cur.execute(query, [user])
    check_user = cur.fetchall()

    if check_user:
        query = "UPDATE users SET password = ? WHERE username = ?"
        cur.execute(query, [password_hash.hexdigest(), user])
        conn.commit()
        conn.close()
        return jsonify({'Success': 'Password changed'}), 201


app.run()
