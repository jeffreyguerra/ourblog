from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()



#Creates User DB
session.execute(
    """CREATE TABLE users(
 	 id INTEGER PRIMARY KEY AUTOINCREMENT,
  	username TEXT NOT NULL,
  	email TEXT NOT NULL,
  	password TEXT NOT NULL
	);

	INSERT INTO users
	(
 	 username,
 	 email,
  	password
	)	
 	 VALUES
 	 (
 	   'tho96',
 	   'abc@example.com',
	    'password'
 	 );"""
)

#Creates Article DB
session.execute(
	"""DROP TABLE IF EXISTS articles;

		CREATE TABLE articles(
		  article_id uuid PRIMARY KEY AUTOINCREMENT,
		  title TEXT NOT NULL,
		  body TEXT NOT NULL,
		  author TEXT NOT NULL,
		  date_added TEXT,
		  last_modified TEXT
		);
		INSERT INTO Articles(
		  title,
		  body,
		  author,
		  date_added,
		  last_modified
		)
		  VALUES
		  (
		    'title 1',
		    'this is the body',
		    'tho96',
		    DATETIME('now','localtime'),
		    DATETIME('now','localtime')
		  );"""
)

#Creates Tag DB
session.execute(
	"""DROP TABLE IF EXISTS tags;
	CREATE TABLE tags (
	url INTEGER,
	tag TEXT,
	PRIMARY KEY(url, tag)
	);"""
)

#Creates Comments DB
session.execute(
	"""DROP TABLE IF EXISTS comments;

	CREATE TABLE comments(
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    url INTEGER NOT NULL,
	    date_added INTEGER NOT NULL,
	    author TEXT NOT NULL,
	    comment TEXT NOT NULL
	 );"""
)
