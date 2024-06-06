CREATE TABLE IF NOT EXISTS user_favorite_tender (
    user_id         VARCHAR(40) NOT NULL REFERENCES users(id),
    tender_id       INT         NOT NULL REFERENCES tender(id),
    PRIMARY KEY (user_id, tender_id)
);

CREATE INDEX IF NOT EXISTS user_favorite_tender_index
ON user_favorite_tender(user_id, tender_id);
