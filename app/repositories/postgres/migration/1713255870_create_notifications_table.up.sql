CREATE TABLE IF NOT EXISTS notifications (
    user_id VARCHAR(40) NOT NULL REFERENCES users(id),
    msg     TEXT        NOT NULL,
    href    TEXT        DEFAULT NULL,
    PRIMARY KEY (user_id)
);