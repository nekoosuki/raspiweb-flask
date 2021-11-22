DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- 测试阶段发现的问题
    devname TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE config(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    devname TEXT NOT NULL,
    conf FLOAT NULL,
    iou FLOAT NULL,
    FOREIGN KEY (devname) REFERENCES user (devname)
);
