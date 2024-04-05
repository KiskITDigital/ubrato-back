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