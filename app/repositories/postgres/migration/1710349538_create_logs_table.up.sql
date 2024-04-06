CREATE TABLE IF NOT EXISTS logs (
    id          VARCHAR(40)     PRIMARY KEY,
    method      VARCHAR(6)      DEFAULT NULL,
    url         VARCHAR(255)    DEFAULT NULL,
    body        TEXT            DEFAULT NULL,
    code        SMALLINT        DEFAULT NULL,
    msg         TEXT            DEFAULT NULL,
    created_at  TIMESTAMPTZ     DEFAULT CURRENT_TIMESTAMP
);