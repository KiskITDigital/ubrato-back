CREATE TABLE IF NOT EXISTS customer_profile (
    org_id          VARCHAR(40)     NOT NULL REFERENCES organizations(id),
    description     TEXT            DEFAULT NULL,
    PRIMARY KEY (org_id)
);