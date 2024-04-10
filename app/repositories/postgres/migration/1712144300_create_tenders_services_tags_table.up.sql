CREATE TABLE IF NOT EXISTS services_groups (
    id      SERIAL      PRIMARY KEY,
    name    VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS services_types (
    id                  SERIAL      PRIMARY KEY,
    name                VARCHAR(90) NOT NULL,
    service_group_id    INT         REFERENCES services_groups(id)
);

CREATE TABLE IF NOT EXISTS tender_services_groups (
    id                  SERIAL  PRIMARY KEY,
    tender_id           INT     REFERENCES tender(id),
    service_group_id    INT     REFERENCES services_groups(id)
);

CREATE TABLE IF NOT EXISTS tender_services_types (
    id                  SERIAL  PRIMARY KEY,
    tender_id           INT     NOT NULL REFERENCES tender(id),
    service_type_id     INT     NOT NULL REFERENCES services_types(id)
);