DROP TABLE IF EXISTS user;
DROP INDEX IF EXISTS devname_index;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    devname TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    isadmin TINYINT DEFAULT 0,
    conf FLOAT NULL,
    iou FLOAT NULL
);

CREATE INDEX devname_index
ON user(devname);
