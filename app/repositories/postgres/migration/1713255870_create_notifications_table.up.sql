CREATE TABLE IF NOT EXISTS notifications (
    id      SERIAL      PRIMARY KEY,
    user_id VARCHAR(40) NOT NULL REFERENCES users(id),
    header  TEXT        DEFAULT NULL,
    msg     TEXT        DEFAULT NULL,
    href    TEXT        DEFAULT NULL,
    read    BOOLEAN     DEFAULT FALSE
);