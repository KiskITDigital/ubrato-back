CREATE TABLE IF NOT EXISTS contractor_services (
    org_id          VARCHAR(40)     NOT NULL REFERENCES organizations(id),
    service_type_id INT             NOT NULL REFERENCES services_types(id),
    price           INT             NOT NULL,
    PRIMARY KEY (org_id, service_type_id)
);