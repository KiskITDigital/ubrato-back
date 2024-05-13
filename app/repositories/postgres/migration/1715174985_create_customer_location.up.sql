CREATE TABLE IF NOT EXISTS customer_locations (
    org_id  VARCHAR(40) NOT NULL REFERENCES organizations(id),
    city_id INT         NOT NULL REFERENCES cities(id),
    PRIMARY KEY (org_id, city_id)
);