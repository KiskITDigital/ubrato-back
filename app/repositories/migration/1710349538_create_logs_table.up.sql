CREATE TABLE IF NOT EXISTS logs (
    id          VARCHAR(40)     PRIMARY KEY,
    method      VARCHAR(6)      NOT NULL,
    url         VARCHAR(255)    NOT NULL,
    body        TEXT            DEFAULT NULL,
    code        SMALLINT        NOT NULL,
    msg         TEXT            DEFAULT NULL,
    created_at   TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);