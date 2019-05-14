import flask, hashlib, sqlite3, datetime
from flask import request, jsonify, g
from cassandra.cluster import Clusterfrom cassandra.cluster import Cluster

app = flask.Flask(__name__)




def user_exists(user):
    cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()
    cur = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cur.execute(query, [user])
    result = cur.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False

@app.route('/articles', methods=['POST'])
def create_article():
	cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()
    data = request.get_json()
    title = data['title']
    body = data['body']
    date = datetime.datetime.now()
    user = request.authorization['username']



    if user_exists(user):
        query = "INSERT INTO articles (title, body, author, date_added, last_modified) VALUES (?, ?, ?, ?, ?)"
        session.execute(query, [title, body, user, date, date])

        session.commit()
        session.close()
        return jsonify({'Success': 'Article created'}), 201



@app.route('/articles/<id>', methods=['GET'])
def get_article(id):
    cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()
    sesson.row_factory = make_dicts
    query = "SELECT * FROM articles WHERE article_id = ?"
    result = session.execute(query, [id]).fetchone()
    conn.close()
    if result:
        return jsonify(result), 201
    else:
        return jsonify({'Error': 'Article not found'}), 404


@app.route('/articles/edit/<id>', methods=['PATCH'])
def edit_article(id):
    data = request.get_json()
    title = data['title']
    body = data['body']
    author = user_exists(request.authorization['username'])
	
	cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()
   

    query = "SELECT * FROM articles WHERE article_id = ?"
    result = session.execute(query, [id]).fetchone()

    if result:
        date = datetime.datetime.now()
        query = "UPDATE articles SET title = ?, body = ?, last_modified = ? WHERE article_id = ?"
        session.execute(query, [title, body, date, id])
        session.commit()
        session.close()
        return jsonify({'Success': 'Article updated'}), 201
    else:
        return jsonify({'Error': 'No permission'}), 409

@app.route('/articles/delete/<id>', methods=['DELETE'])
def delete_article(id):
  	cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()

    query = "SELECT * FROM articles WHERE article_id = ?"
    result = session.execute(query, [id]).fetchone()

    if result:
        query = "DELETE FROM articles WHERE article_id = ?"
        cur.execute(query, [id])
        session.commit()
        session.close()
        return jsonify({'Success': 'Article deleted'}), 201
    else:
        return jsonify({'Error': 'not found'}), 404

@app.route('/articles/recent/<amount>', methods=['GET'])
def view_recent_articles(amount):
 	cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()

    query = "SELECT * FROM articles ORDER BY date_added DESC LIMIT ?"
    result = session.execute(query, [amount]).fetchall()
    session.commit()
    session.close()
    return jsonify(result), 201

@app.route('/articles/recent/meta/<amount>', methods=['GET'])
def get_recent_articles_meta(amount):
  	cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()

    query = "SELECT article_id, title, author, date_added FROM articles ORDER BY date_added DESC LIMIT ?"
    result = session.execute(query, [amount]).fetchall()
    session.commit()
    session.close()
    return jsonify(result), 201


###last-modified article
@app.route('/articles/recent/meta/<amount>', methods=['GET'])
def get_most_recent_article(amount):
    cluster = Cluster(['172.17.0.2'])
	session = cluster.connect()

    query = "SELECT article_id, title, author, date_added FROM articles ORDER BY date_added DESC LIMIT ?"
    result = session.execute(query, [amount]).fetchall()
    session.commit()
    session.close()
    return jsonify(result), 201

app.run()

