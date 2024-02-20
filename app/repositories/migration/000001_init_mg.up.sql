CREATE TABLE IF NOT EXISTS users (
    id          VARCHAR(255)    PRIMARY KEY,
    brand_name  VARCHAR(255),
    inn         VARCHAR(12),
    email       VARCHAR(255)    UNIQUE,
    phone       VARCHAR(20)     UNIQUE,
    password    VARCHAR(255),
    first_name  VARCHAR(100),
    middle_name VARCHAR(100),
    last_name   VARCHAR(100),
    verify      BOOLEAN         DEFAULT FALSE,
    role        SMALLINT        DEFAULT 0,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);
