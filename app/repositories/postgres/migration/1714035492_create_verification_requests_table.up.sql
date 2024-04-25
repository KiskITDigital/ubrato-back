CREATE TABLE IF NOT EXISTS verification_requests (
    id                  VARCHAR(40)     PRIMARY KEY,
    verified            BOOLEAN         DEFAULT NULL,
    msg                 TEXT            DEFAULT NULL,
    user_id             VARCHAR(40)     NOT NULL REFERENCES users(id),
    verified_at         TIMESTAMPTZ     DEFAULT NULL,
    created_at          TIMESTAMPTZ     DEFAULT CURRENT_TIMESTAMP
)