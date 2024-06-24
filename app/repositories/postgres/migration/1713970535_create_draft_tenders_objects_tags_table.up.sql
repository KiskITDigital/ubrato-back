CREATE TABLE IF NOT EXISTS draft_tender_objects_types (
    tender_id           INT         NOT NULL REFERENCES draft_tender(id),
    object_type_id      INT         NOT NULL REFERENCES objects_types(id),
    PRIMARY KEY (tender_id, object_type_id)
);
CREATE INDEX IF NOT EXISTS draft_tender_objects_types_index
ON draft_tender_objects_types (tender_id, object_type_id);