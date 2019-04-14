DROP TABLE IF EXISTS users;

CREATE TABLE users(
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
  );
