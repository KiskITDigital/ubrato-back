CREATE TABLE IF NOT EXISTS documents (
    id      VARCHAR(40)     PRIMARY KEY,
    url     VARCHAR(255)    NOT NULL,
    type    INT             REFERENCES document_types(id),
    user_id VARCHAR(40)     REFERENCES users(id)
);