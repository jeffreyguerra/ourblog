DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS comments;

CREATE TABLE tags (
    url INTEGER,
    tag TEXT,
    PRIMARY KEY(url, tag)
);


CREATE TABLE comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url INTEGER NOT NULL,
    date_added INTEGER NOT NULL,
    author TEXT NOT NULL,
    comment TEXT NOT NULL
 );
