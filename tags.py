import sqlite3
import time

#import BasicAuth
from flask import Flask, jsonify, request
import hashlib

CREATE_DB_FILE = 'createdb.sql'
DATABASE = "database.db"
app = Flask(__name__)

# class bAuth(BasicAuth):
#     def check_credentials(self, username, password):
#         conn = sqlite3.connect(DATABASE)
#         cur = conn.cursor()
#         password_hash = hashlib.md5(password.encode())
#         query = "SELECT * FROM users WHERE username = ? AND password = ?"
#         cur.execute(query, [username, password_hash.hexdigest()])
#         result = cur.fetchall()
#         conn.close()
#         #if (result[0] > 0):
#         if result:
#             return True
#         else:
#             return False
#
# auth = bAuth(app)

@app.cli.command('createdb')
#basicauth
def createdb():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    with open(CREATE_DB_FILE) as queryfile:
        cursor.executescript(queryfile.read())
    conn.close()


#Add tags for a new URL
@app.route('/article/<url>/tags/<tag>', methods=['PUT', 'DELETE'])
# @auth.required
def add_url_and_tag(url, tag):
    if request.method == 'PUT':
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            query = '''SELECT 1
                        FROM articles
                        WHERE id = ?'''
            result = cursor.execute(query, (url)).fetchall()

            if not result:
                return jsonify({"Error": "Article with url doesnt exist"}), 409


            query = '''REPLACE INTO tags(url, tag) VALUES(?, ?)'''
            cursor.execute(query, (url, tag))
            conn.commit()
            conn.close()
            print(query)
            return jsonify({"true": "success"}), 200
        except Exception as exc:
            print(exc)
            return jsonify({"false": "failure"}), 400

    else:
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            query = '''DELETE FROM tags
                        WHERE url = ?
                         AND tag = ?'''
            cursor.execute(query, (url, tag))

            conn.commit()
            conn.close()
            print(query)
            return jsonify({"true": "success"}), 200
        except Exception as exc:
            print(exc)
            return jsonify({"false": "failure"}), 400




@app.route('/article/<url>/tags', methods = ['GET'])
def get_tags_for_url(url):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = '''SELECT tag
    FROM tags WHERE url = ?'''
    all_tags = cursor.execute(query, [url]).fetchall()
    conn.close()
    if all_tags:
        return jsonify(all_tags), 200
    else:
        return jsonify({"Error":"No url with tags exists"}), 404


#Retrieve list of URLs with a given tag
@app.route('/article/tags/<tag>', methods = ['GET'])
def get_urls_with_given_tag(tag):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = '''SELECT  url
        FROM tags
        WHERE tag = ?'''

    cursor.execute(query, [tag])

    results = cursor.fetchall()
    results = [dict(row) for row in results]
    print(type(results))
    print(results)
    output = []

    for item in results:
        output.append(item['url'])

    conn.close()

    print(query)
    return jsonify({"urls": output}), 200
