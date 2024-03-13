CREATE TABLE IF NOT EXISTS documents (
    id              VARCHAR(40)     PRIMARY KEY,
    url             VARCHAR(255)    NOT NULL,
    organization_id VARCHAR(40)     REFERENCES organizations(id)
);