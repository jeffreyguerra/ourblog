import sqlite3

CREATE_USER_DB_FILE = 'create_userdb.sql'
CREATE_ARTICLE_DB_FILE = 'create_articledb.sql'
CREATE_TAG_DB_FILE = 'create_tagdb.sql'
CREATE_COMMENT_DB_FILE = 'create_commentdb.sql'

USER_DATABASE = "user.db"
ARTICLE_DATABASE = "article.db"
TAG_DATABASE = "tag.db"
COMMENT_DATABASE = "comment.db"

#Creates User DB
conn = sqlite3.connect(USER_DATABASE)
cursor = conn.cursor()
with open(CREATE_USER_DB_FILE) as queryfile:
    cursor.executescript(queryfile.read())
conn.close()

#Creates Article DB
conn = sqlite3.connect(ARTICLE_DATABASE)
cursor = conn.cursor()
with open(CREATE_ARTICLE_DB_FILE) as queryfile:
    cursor.executescript(queryfile.read())
conn.close()

#Creates Tag DB
conn = sqlite3.connect(TAG_DATABASE)
cursor = conn.cursor()
with open(CREATE_TAG_DB_FILE) as queryfile:
    cursor.executescript(queryfile.read())
conn.close()

#Creates Comments DB
conn = sqlite3.connect(COMMENT_DATABASE)
cursor = conn.cursor()
with open(CREATE_COMMENT_DB_FILE) as queryfile:
    cursor.executescript(queryfile.read())
conn.close()
