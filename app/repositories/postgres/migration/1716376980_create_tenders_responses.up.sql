CREATE TABLE IF NOT EXISTS tenders_responses (
    tender_id   INT         NOT NULL REFERENCES tender(id),
    user_id     VARCHAR(40) NOT NULL REFERENCES users(id),
    price       INT         DEFAULT NULL,
    respond_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tender_id, user_id)
);