CREATE TABLE IF NOT EXISTS sessions (
    id          VARCHAR(32) PRIMARY KEY,
    user_id     VARCHAR(40) NOT NULL REFERENCES users(id),
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
