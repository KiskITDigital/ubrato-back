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
    id              VARCHAR(40)     PRIMARY KEY,
    url             VARCHAR(255)    NOT NULL,
    organization_id VARCHAR(40)     REFERENCES organizations(id)
);


CREATE TABLE IF NOT EXISTS objects_groups (
    id      SERIAL      PRIMARY KEY,
    name    VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS services_groups (
    id      SERIAL      PRIMARY KEY,
    name    VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS objects_types (
    id              SERIAL      PRIMARY KEY,
    name            VARCHAR(40) NOT NULL,
    object_group_id INT 		REFERENCES objects_groups(id)
);

CREATE TABLE IF NOT EXISTS services_types (
    id                  SERIAL      PRIMARY KEY,
    name                VARCHAR(90) NOT NULL,
    service_group_id    INT         REFERENCES services_groups(id)
);

CREATE TABLE IF NOT EXISTS tender (
    id              VARCHAR(40)     PRIMARY KEY,
    name            VARCHAR(255)    NOT NULL,
    regions         TEXT[]          NOT NULL,
    floor_space     INT             NOT NULL,
    description     VARCHAR(400)    NULL,
    wishes          VARCHAR(400)    NULL,
    attachments     TEXT[]          NULL,
    services_groups INTEGER[]       NULL,
    services_types  INTEGER[]       NULL,
    reception_start TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    reception_end   TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    work_start      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    work_end        TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    object_group_id INT 		    REFERENCES objects_groups(id),
    object_type_id  INT 		    REFERENCES objects_types(id),
    user_id         VARCHAR(40)     NOT NULL REFERENCES users(id),
    created_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    id          VARCHAR(40)     PRIMARY KEY,
    method      VARCHAR(6)      NOT NULL,
    url         VARCHAR(255)    NOT NULL,
    body        TEXT            DEFAULT NULL,
    code        SMALLINT        NOT NULL,
    msg         TEXT            DEFAULT NULL,
    created_at   TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);
