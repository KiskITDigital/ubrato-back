CREATE TABLE IF NOT EXISTS users (
    id              VARCHAR(40)     PRIMARY KEY,
    email           VARCHAR(255)    NOT NULL UNIQUE,
    phone           VARCHAR(20)     NOT NULL UNIQUE,
    password        VARCHAR(255)    NOT NULL,
    totp_salt       VARCHAR(32)     NOT NULL,
    first_name      VARCHAR(100)    NOT NULL,
    middle_name     VARCHAR(100)    NOT NULL,
    last_name       VARCHAR(100)    NOT NULL,
    avatar          VARCHAR(255)    NOT NULL,
    verified        BOOLEAN         DEFAULT FALSE,
    email_verified  BOOLEAN         DEFAULT FALSE,
    role            SMALLINT        DEFAULT 0,
    is_contractor   BOOLEAN         DEFAULT FALSE,
    created_at      TIMESTAMPTZ     DEFAULT CURRENT_TIMESTAMP
);