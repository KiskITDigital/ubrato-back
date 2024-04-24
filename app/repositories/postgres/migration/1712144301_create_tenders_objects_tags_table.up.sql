CREATE TABLE IF NOT EXISTS objects_groups (
    id      SERIAL      PRIMARY KEY,
    name    VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS objects_types (
    id              SERIAL      PRIMARY KEY,
    name            VARCHAR(40) NOT NULL,
    object_group_id INT 		REFERENCES objects_groups(id)
);

CREATE TABLE IF NOT EXISTS tender_objects_types (
    tender_id           INT     NOT NULL REFERENCES tender(id),
    object_type_id      INT     NOT NULL REFERENCES objects_types(id),
    PRIMARY KEY (tender_id, object_type_id)
);
CREATE INDEX IF NOT EXISTS tender_objects_types_index
ON tender_objects_types (tender_id, object_type_id);