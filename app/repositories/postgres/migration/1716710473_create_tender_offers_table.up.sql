CREATE TABLE IF NOT EXISTS tender_offers (
    contractor_id   VARCHAR(40) NOT NULL REFERENCES organizations(id),
    tender_id       INT         NOT NULL REFERENCES tender(id),
    PRIMARY KEY (contractor_id, tender_id)
);

CREATE INDEX IF NOT EXISTS tender_offers_index
ON tender_offers(contractor_id, tender_id);
