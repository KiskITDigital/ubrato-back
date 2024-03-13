CREATE TABLE IF NOT EXISTS users (
    id          VARCHAR(40)     PRIMARY KEY,
    email       VARCHAR(255)    NOT NULL UNIQUE,
    phone       VARCHAR(20)     NOT NULL UNIQUE,
    password    VARCHAR(255)    NOT NULL,
    first_name  VARCHAR(100)    NOT NULL,
    middle_name VARCHAR(100)    NOT NULL,
    last_name   VARCHAR(100)    NOT NULL,
    verify      BOOLEAN         DEFAULT FALSE,
    role        SMALLINT        DEFAULT 0,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);