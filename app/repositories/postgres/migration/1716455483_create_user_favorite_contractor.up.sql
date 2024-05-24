CREATE TABLE IF NOT EXISTS user_favorite_contractor (
    contractor_id   VARCHAR(40) NOT NULL REFERENCES organizations(id),
    user_id         VARCHAR(40) NOT NULL REFERENCES users(id),
    PRIMARY KEY (contractor_id, user_id)
);

CREATE INDEX IF NOT EXISTS user_favorite_contractor_index
ON user_favorite_contractor(user_id, contractor_id);
