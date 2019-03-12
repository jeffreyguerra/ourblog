from flask import Flask, jsonify, abort, render_template, flash, redirect, url_for, session, request, logging

import sqlite3


CREATE_DB_FILE = 'createdb.sql'
DATABASE = "database.db"
app = Flask(__name__)




@app.cli.command('createdb')
def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    with open(CREATE_DB_FILE) as queryfile:
        cursor.executescript(queryfile.read())
    conn.close()

@app.route('/')
def hello_world():
    return jsonify({"key":"yolo"})
    return abort(404)


#Add tags for a new URL
@app.route('/article/<url>/tags/<tag>', methods=['PUT', 'DELETE'])
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

# #############################Start of comments.. Post new comment on an article#####
# @app.route('/article/<url>/comments', methods = ['POST'])
# def post_comment(url):
#     try:
#         conn = sqlite3.connect(DATABASE)
#         cursor = conn.cursor()
#         query = '''SELECT 1
#               FROM articles
#               WHERE id = ?'''
#         result = cursor.execute(query, (url)).fetchall()
#
#
#         if not result:
#             return jsonify({"Error": "Article with url doesnt exist"}), 409
#         #Above is checking if comment can even be made, che cking if article exists
#         #Now post new comment
#
#         query = '''INSERT INTO TABLE(comments,([id?]) )'''
#
#         conn.close()
#         print(query)
#         return jsonify({"true": "success"}), 200
#     except Exception as exc:
#         print(exc)
#         return jsonify({"false": "failure"}), 400
#
# # CREATE TABLE comments(
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     date_added INTEGER NOT NULL,
# #     author TEXT NOT NULL
# # );
#
# @app.route('/article/<url>/comments/<id>', methods = ['DELETE'])
# def delete_Comment(url, id):
#     # Delete an individual comment
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     query = '''DELETE FROM comments
#                 WHERE id = ?'''
#     cursor.execute(query, (id))
#
#     conn.commit()
#     conn.close()
# ####Get number of comments on a given article
# @app.route('/article/<id>/comments/counts', methods = ['GET'])
# def get_number_of_comments(id):
#
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#
#     query = '''SELECT COUNT(*) AS COUNT
#         FROM comments
#         WHERE id = ?
#         GROUP BY id'''
#
#
#     cursor.execute(query, [id])
#
#     results = cursor.fetchall()
#     results = [dict(row) for row in results] ##??
#     print(type(results))
#     print(results)
#
#     count = results['COUNT']
#     conn.close()
#
#     print(query)
#     return jsonify({"count": count}), 200 #???
#
# ####GET n most recent comments on a URL
# @app.route('/article/<id>/comments/recent')
# def get_number_most_recent_comments(id): ###??
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#
#     query = '''SELECT comment
#         FROM comments
#         WHERE id = ?
#         '''
#     cursor.execute(query, [id])
#
#     results = cursor.fetchall()
#     results = [dict(row) for row in results]
#
#     output = []
#
#     for item in results:
#         output.append(item['comment'])
#
#     return jsonify({'comments': output}), 200