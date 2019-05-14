import sqlite3
import time
from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
import hashlib

app = Flask(__name__)


@app.route('/article/<url>/comments', methods = ['POST'])
def post_comment(url):
    try:
        cluster = Cluster(['172.17.0.2'])
    	session = cluster.connect()
        query = '''SELECT 1
              FROM articles
              WHERE id = ?'''
        result = session.execute(query, (url)).fetchall()


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

        session.execute(query, (url, epoch_time, author, comment))
        session.commit()

        id = cursor.lastrowid

        session.close()

        return jsonify({"id": id}), 200
    except Exception as exc:
        print(exc)
        return jsonify({"false": "failure"}), 400

@app.route('/article/<url>/comments/<id>', methods = ['DELETE'])
# @auth.required
def delete_Comment(url, id):
    # Delete an individual comment
 	cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    try:
        query = '''DELETE FROM comments
                    WHERE id = ?
                    AND url = ?'''
        session.execute(query, (id, url))

        session.commit()
    except:
        return jsonify({"Error": "Comment didnt exist"}), 404
    session.close()
    return jsonify({"success": "Comment deleted"}), 200

####Get number of comments on a given article
@app.route('/article/comments/count/<id>', methods = ['GET'])
def get_number_of_comments(id):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()

    query = '''SELECT COUNT(*) AS COUNT
        FROM comments
        WHERE id = ?
        '''

    session.execute(query, [id])

    results = session.fetchone()
    results = dict(results)
    count = results['COUNT']
    session.close()

    print(query)
    return jsonify({"count": count}), 200

####GET n most recent comments on a URL
@app.route('/article/comments/<url>', methods = ['GET'])
def get_number_most_recent_comments(url):

    limit = request.args.get('limit')
    if not limit:
        return jsonify({"Error": "Please provide limit in query string e.g. ?limit=10"}), 200

    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()

    query = '''SELECT id, url, date_added, author, comment
                FROM comments
                WHERE url = ?
                ORDER BY ID ASC
                LIMIT ?;'''
    session.execute(query, [url, limit])

    results = cursor.fetchall()
    results = [dict(row) for row in results]

    for item in results:
        item['date_added'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['date_added']))

    return jsonify({'comments': results}), 200

@app.route('/article/comments/Last-Modified', methods = ['GET'])
#p3
def get_most_recent_comment(url, id): 
#here press 1

    limit = request.args.get('limit')
    if not limit:
        return jsonify({"Error": "Please provide limit in query string e.g. ?limit=10"}), 200

    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()

    query = '''SELECT id, url, date_added, author, comment
                FROM comments
                WHERE url = ?
                ORDER BY ID ASC
                LIMIT ?;'''
    session.execute(query, [url, limit])

    results = session.fetchall()
    results = [dict(row) for row in results]

    for item in results:
        item['date_added'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['date_added']))

    return jsonify({'comments': results}), 200


