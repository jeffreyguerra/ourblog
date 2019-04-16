import sqlite3
import time

#import BasicAuth
from flask import Flask, jsonify, request
import hashlib

DATABASE = "comment.db"
app = Flask(__name__)


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
@app.route('/article/comments/count/<id>', methods = ['GET'])
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
@app.route('/article/comments/<url>', methods = ['GET'])
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
