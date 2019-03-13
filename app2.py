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

@app.route('/article/<url>/comments', methods = ['POST'])
def post_comment(url):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        query = '''SELECT 1
              FROM articles
              WHERE id = ?'''
        result = cursor.execute(query, (url)).fetchall()


        if not result:
            return jsonify({"Error": "Article with url doesnt exist"}), 409
        #Above is checking if comment can even be made, checking if article exists
        #Now post new comment

        query = '''INSERT INTO comments (url, date_added, author, comment) VALUES (?, ?, ?, ?)'''
        epoch_time = int(time.time())
        if 'username' in request.headers:
            author = request.headers['username']
        else:
            author = 'Anon'

        data = request.get_json()
        if 'comment' in data:
            comment = data['comment']
        else:
            return jsonify({"Error": "No comment"}), 400

        cursor.execute(query, (url, epoch_time, author, comment))
        conn.commit()

        id = cursor.lastrowid

        conn.close()

        return jsonify({"id": id}), 200
    except Exception as exc:
        print(exc)
        return jsonify({"false": "failure"}), 400

@app.route('/article/<url>/comments/<id>', methods = ['DELETE'])
# @auth.required
def delete_Comment(url, id):
    # Delete an individual comment
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        query = '''DELETE FROM comments
                    WHERE id = ?
                    AND url = ?'''
        cursor.execute(query, (id, url))

        conn.commit()
    except:
        return jsonify({"Error": "Comment didnt exist"}), 404
    conn.close()
    return jsonify({"success": "Comment deleted"}), 200

####Get number of comments on a given article
@app.route('/article/<id>/comments/count', methods = ['GET'])
def get_number_of_comments(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = '''SELECT COUNT(*) AS COUNT
        FROM comments
        WHERE id = ?
        '''

    cursor.execute(query, [id])

    results = cursor.fetchone()
    results = dict(results)
    count = results['COUNT']
    conn.close()

    print(query)
    return jsonify({"count": count}), 200

####GET n most recent comments on a URL
@app.route('/article/<url>/comments', methods = ['GET'])
def get_number_most_recent_comments(url):

    limit = request.args.get('limit')
    if not limit:
        return jsonify({"Error": "Please provide limit in query string e.g. ?limit=10"}), 200

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = '''SELECT id, url, date_added, author, comment 
                FROM comments 
                WHERE url = ?
                ORDER BY ID ASC
                LIMIT ?;'''
    cursor.execute(query, [url, limit])

    results = cursor.fetchall()
    results = [dict(row) for row in results]

    for item in results:
        item['date_added'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['date_added']))

    return jsonify({'comments': results}), 200