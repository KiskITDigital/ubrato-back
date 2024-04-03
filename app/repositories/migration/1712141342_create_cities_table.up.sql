CREATE TABLE IF NOT EXISTS cities (
    id            SERIAL          PRIMARY KEY,
    name          VARCHAR(255)    NOT NULL,
    region_id     INT             REFERENCES regions(id)
);
