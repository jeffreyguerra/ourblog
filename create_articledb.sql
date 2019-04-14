DROP TABLE IF EXISTS articles;

CREATE TABLE articles(
  article_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
  );
