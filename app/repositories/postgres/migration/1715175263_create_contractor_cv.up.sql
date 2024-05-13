CREATE TABLE IF NOT EXISTS contractor_cv (
    id              VARCHAR(40)     PRIMARY KEY,
    org_id          VARCHAR(40)     NOT NULL REFERENCES organizations(id),
    name            VARCHAR(50)     NOT NULL,
    description     TEXT            NOT NULL,
    links           TEXT[]          NOT NULL
);