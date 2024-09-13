CREATE TABLE IF NOT EXISTS organizations (
    id                  VARCHAR(40)     PRIMARY KEY,
    brand_name          VARCHAR(255)    NOT NULL,
    full_name           VARCHAR(255)    NOT NULL,
    short_name          VARCHAR(50)     NOT NULL,
    inn                 VARCHAR(12)     NOT NULL UNIQUE,
    okpo                VARCHAR(8)      NOT NULL,
    ogrn                VARCHAR(15)     NOT NULL,
    kpp                 VARCHAR(9)      NOT NULL,
    tax_code            INT             NOT NULL,
    address             VARCHAR(255)    NOT NULL,
    avatar              VARCHAR(255)    DEFAULT NULL,
    email               JSONB           DEFAULT '[]'::jsonb,
    phone               JSONB           DEFAULT '[]'::jsonb,
    messenger           JSONB           DEFAULT '[]'::jsonb,
    user_id             VARCHAR(40)     NOT NULL REFERENCES users(id),
    update_at           TIMESTAMPTZ     DEFAULT CURRENT_TIMESTAMP,
    created_at          TIMESTAMPTZ     DEFAULT CURRENT_TIMESTAMP
);
