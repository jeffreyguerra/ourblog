DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS articles;

CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE articles(
  article_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  author TEXT NOT NULL,
  date_added TEXT,
  last_modified TEXT
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
    (select username from users where username = 'tho96'),
    DATETIME('now','localtime'),
    DATETIME('now','localtime')
  );
commit;
