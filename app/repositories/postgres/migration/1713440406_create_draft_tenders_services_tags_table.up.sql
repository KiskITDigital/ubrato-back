CREATE TABLE IF NOT EXISTS draft_tender_services_types (
    tender_id           INT         NOT NULL REFERENCES draft_tender(id),
    service_type_id     INT         NOT NULL REFERENCES services_types(id),
    PRIMARY KEY (tender_id, service_type_id)
);
CREATE INDEX IF NOT EXISTS draft_tender_services_types_index
ON draft_tender_services_types (tender_id, service_type_id);