DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    devname TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE config(
    devname TEXT PRIMARY KEY,
    conf FLOAT NULL,
    iou FLOAT NULL,
    FOREIGN KEY (devname) REFERENCES user (devname)
);
