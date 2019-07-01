DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Status(
  user_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  projectName TEXT NOT NULL,
  day DATE NOT NULL,
  statusEmp TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (name) REFERENCES user (username)
);
