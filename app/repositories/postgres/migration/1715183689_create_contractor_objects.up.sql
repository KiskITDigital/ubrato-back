CREATE TABLE IF NOT EXISTS contractor_objects (
    org_id          VARCHAR(40)     NOT NULL REFERENCES organizations(id),
    object_type_id  INT             NOT NULL REFERENCES objects_types(id),
    PRIMARY KEY (org_id, object_type_id)
);