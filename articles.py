import flask, hashlib, sqlite3, datetime
from flask import request, jsonify, g


app = flask.Flask(__name__)
DATABASE = 'article.db'



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

def user_exists(user):
    conn = sqlite3.connect(DATABASE)
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
    data = request.get_json()
    title = data['title']
    body = data['body']
    date = datetime.datetime.now()
    user = request.authorization['username']


    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    if user_exists(user):
        query = "INSERT INTO articles (title, body, author, date_added, last_modified) VALUES (?, ?, ?, ?, ?)"
        cur.execute(query, [title, body, user, date, date])

        conn.commit()
            # id = cur.lastrowid
        conn.close()
        return jsonify({'Success': 'Article created'}), 201



@app.route('/articles/<id>', methods=['GET'])
def get_article(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    cur = conn.cursor()
    query = "SELECT * FROM articles WHERE article_id = ?"
    result = cur.execute(query, [id]).fetchone()
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

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    cur = conn.cursor()

    query = "SELECT * FROM articles WHERE article_id = ?"
    result = cur.execute(query, [id]).fetchone()

    if result:
        date = datetime.datetime.now()
        query = "UPDATE articles SET title = ?, body = ?, last_modified = ? WHERE article_id = ?"
        cur.execute(query, [title, body, date, id])
        conn.commit()
        conn.close()
        return jsonify({'Success': 'Article updated'}), 201
    else:
        return jsonify({'Error': 'No permission'}), 409

@app.route('/articles/delete/<id>', methods=['DELETE'])
def delete_article(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    cur = conn.cursor()

    query = "SELECT * FROM articles WHERE article_id = ?"
    result = cur.execute(query, [id]).fetchone()

    if result:
        query = "DELETE FROM articles WHERE article_id = ?"
        cur.execute(query, [id])
        conn.commit()
        conn.close()
        return jsonify({'Success': 'Article deleted'}), 201
    else:
        return jsonify({'Error': 'not found'}), 404

@app.route('/articles/recent/<amount>', methods=['GET'])
def view_recent_articles(amount):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    cur = conn.cursor()

    query = "SELECT * FROM articles ORDER BY date_added DESC LIMIT ?"
    result = cur.execute(query, [amount]).fetchall()
    conn.commit()
    conn.close()
    return jsonify(result), 201

@app.route('/articles/recent/meta/<amount>', methods=['GET'])
def get_recent_articles_meta(amount):
    #amount = request.args['amount']

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    cur = conn.cursor()

    query = "SELECT article_id, title, author, date_added FROM articles ORDER BY date_added DESC LIMIT ?"
    result = cur.execute(query, [amount]).fetchall()
    conn.commit()
    conn.close()
    return jsonify(result), 201

app.run()
