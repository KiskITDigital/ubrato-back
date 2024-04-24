CREATE TABLE IF NOT EXISTS draft_tender_objects_types (
    tender_id           INT     NOT NULL REFERENCES tender(id),
    object_type_id     INT      NOT NULL REFERENCES objects_types(id),
    PRIMARY KEY (tender_id, object_type_id)
);
CREATE INDEX IF NOT EXISTS draft_tender_objects_types_index
ON tender_objects_types (tender_id, object_type_id);