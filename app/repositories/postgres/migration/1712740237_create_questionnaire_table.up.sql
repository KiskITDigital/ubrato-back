CREATE TABLE IF NOT EXISTS questionnaire (
    id          SERIAL          PRIMARY KEY,
    answers     TEXT[]          NULL,
    user_id     VARCHAR(40)     NOT NULL REFERENCES users(id) UNIQUE,
    created_at  TIMESTAMPTZ     DEFAULT CURRENT_TIMESTAMP
);
