DROP TABLE IF EXISTS tags;

CREATE TABLE tags (
    url INTEGER,
    tag TEXT,
    PRIMARY KEY(url, tag)
);
