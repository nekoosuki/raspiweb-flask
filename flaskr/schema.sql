DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- 测试阶段发现的问题
    devname TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    isadmin TINYINT DEFAULT 0
);

CREATE TABLE config(
    devname TEXT PRIMARY KEY,
    conf FLOAT NULL,
    iou FLOAT NULL,
    FOREIGN KEY (devname) REFERENCES user (devname)
);
