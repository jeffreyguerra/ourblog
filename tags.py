import sqlite3
import time
from cassandra.cluster import Cluster
from flask import Flask, jsonify, request
import hashlib

app = Flask(__name__)




#Add tags for a new URL
@app.route('/article/<url>/tags/<tag>', methods=['PUT', 'DELETE'])
# @auth.required
def add_url_and_tag(url, tag):
    if request.method == 'PUT':
        try:
            cluster = Cluster(['172.17.0.2'])
   			session = cluster.connect()
            query = '''REPLACE INTO tags(url, tag) VALUES(?, ?)'''
            session.execute(query, (url, tag))
            session.commit()
            session.close()
            print(query)
            return jsonify({"true": "success"}), 200
        except Exception as exc:
            print(exc)
            return jsonify({"false": "failure"}), 400

    else:
        try:
            cluster = Cluster(['172.17.0.2'])
   			session = cluster.connect()
            query = '''DELETE FROM tags
                        WHERE url = ?
                         AND tag = ?'''
            session.execute(query, (url, tag))

            session.commit()
            session.close()
            print(query)
            return jsonify({"true": "success"}), 200
        except Exception as exc:
            print(exc)
            return jsonify({"false": "failure"}), 400




@app.route('/article/<url>/tags', methods = ['GET'])
def get_tags_for_url(url):
    cluster = Cluster(['172.17.0.2'])
   	session = cluster.connect()

    query = '''SELECT tag
    FROM tags WHERE url = ?'''
    all_tags = session.execute(query, [url]).fetchall()
    session.close()
    if all_tags:
        return jsonify(all_tags), 200
    else:
        return jsonify({"Error":"No url with tags exists"}), 404


#Retrieve list of URLs with a given tag
@app.route('/article/tags/<tag>', methods = ['GET'])
def get_urls_with_given_tag(tag):

    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()

    query = '''SELECT  url
        FROM tags
        WHERE tag = ?'''

    session.execute(query, [tag])

    results = session.fetchall()
    results = [dict(row) for row in results]
    print(type(results))
    print(results)
    output = []

    for item in results:
        output.append(item['url'])

    session.close()

    print(query)
    return jsonify({"urls": output}), 200
