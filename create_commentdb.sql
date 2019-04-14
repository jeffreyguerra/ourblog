DROP TABLE IF EXISTS comments;

CREATE TABLE comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url INTEGER NOT NULL,
    date_added INTEGER NOT NULL,
    author TEXT NOT NULL,
    comment TEXT NOT NULL
 );
