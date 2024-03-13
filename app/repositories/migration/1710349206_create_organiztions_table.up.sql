CREATE TABLE IF NOT EXISTS organizations (
    id                  VARCHAR(40)     PRIMARY KEY,
    brand_name          VARCHAR(255)    NOT NULL,
    short_name          VARCHAR(50)     NOT NULL,
    inn                 VARCHAR(12)     NOT NULL UNIQUE,
    okpo                VARCHAR(8)      NOT NULL UNIQUE,
    orgn                VARCHAR(15)     NOT NULL UNIQUE,
    kpp                 VARCHAR(9)      NOT NULL UNIQUE,
    tax_code            INT             NOT NULL,
    real_address        VARCHAR(255)    NOT NULL,
    registered_address  VARCHAR(255)    NOT NULL,
    mail_address        VARCHAR(255)    NOT NULL,
    user_id             VARCHAR(40)     NOT NULL REFERENCES users(id),
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);
