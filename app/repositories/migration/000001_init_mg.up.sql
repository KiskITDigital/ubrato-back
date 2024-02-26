CREATE TABLE IF NOT EXISTS users (
    id          VARCHAR(40)     PRIMARY KEY,
    email       VARCHAR(255)    NOT NULL UNIQUE,
    phone       VARCHAR(20)     NOT NULL UNIQUE,
    password    VARCHAR(255)    NOT NULL,
    first_name  VARCHAR(100)    NOT NULL,
    middle_name VARCHAR(100)    NOT NULL,
    last_name   VARCHAR(100)    NOT NULL,
    verify      BOOLEAN         DEFAULT FALSE,
    role        SMALLINT        DEFAULT 0,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

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

CREATE TABLE IF NOT EXISTS documents (
    id              VARCHAR(40) PRIMARY KEY,
    url             VARCHAR(255) NOT NULL,
    organization_id VARCHAR(40) REFERENCES organizations(id)
);